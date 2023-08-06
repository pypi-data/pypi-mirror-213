import asyncio
import os
import random
import re
import string
import types
from unittest.mock import AsyncMock, Mock, call, patch

import aiobtclientrpc
import pytest

from aiobtclientapi import errors, utils
from aiobtclientapi.clients import base


class MyURL(aiobtclientrpc.URL):
    default = 'mybt://localhost:123'


class MyRPC(aiobtclientrpc.RPCBase):
    label = 'MyBT'
    name = 'mybt'
    URL = MyURL
    _call = AsyncMock()
    _connect = AsyncMock()
    _disconnect = AsyncMock()


def MyAPI():
    class MyAPI(base.APIBase, MyRPC):
        _get_infohashes = Mock()
        _get_torrent_fields = AsyncMock()
        _add_torrent = Mock()
        _start_torrent = Mock()
        _stop_torrent = Mock()
        _torrent_is_verifying = AsyncMock()
        _start_verifying = AsyncMock()
        _get_verifying_progress = AsyncMock()

    return MyAPI()


@pytest.fixture
def do_method_tests(mocker):
    """Run tests for api.add(), api.start(), api.stop(), etc"""

    async def do_method_tests(
            method_name=None, method_args=(), method_kwargs={},
            method_wrapper_name=None, exp_method_wrapper_args=(), exp_method_wrapper_kwargs={},
            attributes={}, types={}, exception_cls=None,
    ):
        from_call_mock = mocker.patch('aiobtclientapi.response.Response.from_call')
        mocker.patch(f'aiobtclientapi.clients.APIBase.{method_wrapper_name}')

        api = MyAPI()
        method = getattr(api, method_name)
        method_wrapper = getattr(api, method_wrapper_name)

        return_value = await method(*method_args, **method_kwargs)
        assert return_value is from_call_mock.return_value

        assert method_wrapper.call_args_list == [call(*exp_method_wrapper_args, **exp_method_wrapper_kwargs)]
        assert from_call_mock.call_args_list == [call(
            method_wrapper.return_value,
            attributes=attributes,
            types=types,
            exception=exception_cls,
        )]

    return do_method_tests


@pytest.fixture
def do_method_wrapper_tests(mocker):
    """
    Run tests for api._add_torrents(), api._start_torrents(),
    api._stop_torrents(), etc
    """

    async def do_method_wrapper_tests(
            method_name, action_name, *,
            accepts_arbitrary_kwargs,
            takes_infohash,
    ):
        yields = [
            'foo',
            errors.Error('no'),
            'bar',
            errors.Warning('maybe'),
            'baz',
            RuntimeError('argh'),
            'never yielded',
        ]

        api = MyAPI()
        if takes_infohash:
            mocker.patch.object(api, '_normalize_infohash', Mock(side_effect=lambda h: f'normalized:{h}'))
        method = getattr(api, method_name)
        action = mocker.patch.object(api, action_name)
        action.return_value = AsyncMock(
            __class__=types.AsyncGeneratorType,
            __aiter__=lambda self: self,
            __anext__=AsyncMock(side_effect=list(yields)),
        )

        if takes_infohash:
            posargs = [f'infohash{i}' for i in range(1, 100)]
        else:
            posargs = [f'arg{i}' for i in range(1, 100)]

        if accepts_arbitrary_kwargs:
            def random_string():
                return ''.join(random.choice(string.ascii_lowercase)
                               for _ in range(random.randint(3, 12)))

            kwargs = {
                random_string(): random_string()
                for _ in range(random.randint(1, 6))
            }
        else:
            kwargs = {}

        with pytest.raises(RuntimeError, match=r'^argh$'):
            async for yielded in method(posargs, **kwargs):
                assert yielded == yields.pop(0)
        yields.pop(0)  # Remove RuntimeError
        assert yields == ['never yielded']

        if takes_infohash:
            assert action.call_args_list == [
                call('normalized:' + posargs[0], **kwargs),
                call('normalized:' + posargs[1], **kwargs),
                call('normalized:' + posargs[2], **kwargs),
            ]
        else:
            assert action.call_args_list == [
                call(posargs[0], **kwargs),
                call(posargs[1], **kwargs),
                call(posargs[2], **kwargs),
            ]

    return do_method_wrapper_tests


@pytest.mark.asyncio
async def test_init_raises_ValueError(mocker):
    mocker.patch('aiobtclientrpc.RPCBase.__init__', side_effect=ValueError('foo'))
    with pytest.raises(errors.ValueError, match=r'^foo$'):
        MyAPI()


@pytest.mark.asyncio
async def test_context_manager(mocker):
    mocker.patch('aiobtclientapi.clients.APIBase.wait_for_background_tasks')
    mocker.patch('aiobtclientapi.clients.APIBase.disconnect')

    api = MyAPI()
    async with api as api_:
        assert api.wait_for_background_tasks.call_args_list == []
        assert api.disconnect.call_args_list == []
        assert api is api_
    assert api.wait_for_background_tasks.call_args_list == [call()]
    assert api.disconnect.call_args_list == [call()]


@pytest.mark.parametrize('detach, exp_detached', ((0, False), ('yes', True)))
@pytest.mark.parametrize(
    argnames='name, exp_name',
    argvalues=(
        (None, '{func} [{id}]'),
        ('foo', 'foo'),
    ),
)
@pytest.mark.asyncio
async def test_create_background_task(name, exp_name, detach, exp_detached):
    coro_blocker = asyncio.Event()
    coro = AsyncMock(side_effect=coro_blocker.wait)()

    api = MyAPI()
    task = api.create_background_task(coro, name=name, detach=detach)

    # Test `name`
    assert task.get_name() == exp_name.format(func=coro.__qualname__, id=id(coro))

    # Test taskinfo being added to internal list
    assert len(api._background_tasks) == 1
    assert api._background_tasks[0].task is task
    assert api._background_tasks[0].detached is exp_detached

    # Unblock task and wait for it
    assert not task.done()
    asyncio.get_running_loop().call_soon(coro_blocker.set)
    await task
    assert task.done()

    # Task must be removed from internal list
    assert len(api._background_tasks) == 0


@pytest.mark.parametrize(
    argnames='exception, done_callback',
    argvalues=(
        (None, None),
        (None, Mock()),
        (RuntimeError('argh'), None),
        (RuntimeError('argh'), Mock()),
        (asyncio.CancelledError(), None),
        (asyncio.CancelledError(), Mock()),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
# The `mocker` fixture from pytest-mock mock sys.exit() for some reason.
@patch('sys.exit')
async def test_create_background_tasks_handles_exception_from_coro(exit_mock, exception, done_callback, capsys):
    api = MyAPI()
    coro = AsyncMock(side_effect=exception)()
    task = api.create_background_task(coro, done_callback=done_callback)

    if exception:
        with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
            await task
        if done_callback:
            assert done_callback.call_args_list == []
    else:
        await task
        if done_callback:
            assert done_callback.call_args_list == [call(task.result())]

    if exception and not isinstance(exception, asyncio.CancelledError):
        captured = capsys.readouterr()
        assert 'Traceback (most recent call last):' in captured.err
        assert f'{type(exception).__name__}: {str(exception)}' in captured.err
        assert exit_mock.call_args_list == [call(99)]


@pytest.mark.parametrize(
    argnames='exception',
    argvalues=(
        RuntimeError('argh'),
        KeyboardInterrupt('argh'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
# The `mocker` fixture from pytest-mock mock sys.exit() for some reason.
@patch('sys.exit')
async def test_create_background_tasks_handles_exception_from_callback(exit_mock, exception, capsys):
    api = MyAPI()
    coro = AsyncMock()()
    done_callback_wrapper = Mock(side_effect=exception)
    task = api.create_background_task(coro, done_callback=done_callback_wrapper)

    await task
    assert task.done()
    assert done_callback_wrapper.call_args_list == [call(task.result())]

    captured = capsys.readouterr()
    assert 'Traceback (most recent call last):' in captured.err
    assert f'{type(exception).__name__}: {str(exception)}' in captured.err
    assert exit_mock.call_args_list == [call(99)]


@pytest.mark.parametrize('undetached_task_raises_CancelledError', (False, True))
@pytest.mark.asyncio
async def test_wait_for_background_tasks(undetached_task_raises_CancelledError, mocker):
    api = MyAPI()
    unblocker = asyncio.Event()
    tasks = [
        api.create_background_task(
            coro=AsyncMock(side_effect=unblocker.wait)(),
            name='foo',
            detach=False,
        ),
        api.create_background_task(
            coro=AsyncMock(side_effect=unblocker.wait)(),
            name='bar',
            detach=True,
        ),
        api.create_background_task(
            coro=AsyncMock(side_effect=unblocker.wait)(),
            name='baz',
            detach=False,
        ),
    ]
    if undetached_task_raises_CancelledError:
        tasks.append(
            api.create_background_task(
                # Task is cancelled but not detached
                coro=AsyncMock(side_effect=asyncio.CancelledError())(),
                name='asdf',
                detach=False,
            ),
        )

    # Unblock tasks
    asyncio.get_running_loop().call_soon(unblocker.set)

    # Wait for tasks to finish
    if undetached_task_raises_CancelledError:
        with pytest.raises(asyncio.CancelledError):
            await api.wait_for_background_tasks()
    else:
        await api.wait_for_background_tasks()

    assert all(t.done() for t in tasks)

    assert not tasks[0].cancelled()
    assert tasks[1].cancelled()
    assert not tasks[2].cancelled()


@pytest.mark.parametrize(
    argnames='return_value, exception, exp_result',
    argvalues=(
        ('foo', None, 'foo'),
        (None, aiobtclientrpc.ConnectionError('no net'), errors.ConnectionError('no net: {url}')),
        (None, aiobtclientrpc.TimeoutError('timeout'), errors.TimeoutError('timeout: {url}')),
        (None, aiobtclientrpc.AuthenticationError('bad password'), errors.AuthenticationError('bad password: {url}')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_call(return_value, exception, exp_result, mocker):
    call_mock = mocker.patch('aiobtclientrpc.RPCBase.call', side_effect=exception, return_value=return_value)

    api = MyAPI()
    if isinstance(exp_result, Exception):
        exp_msg = str(exp_result).format(url=api.url)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(exp_msg)}$'):
            await api.call(foo='bar', baz=123)
    else:
        retval = await api.call(foo='bar', baz=123)
        assert retval == exp_result

    assert call_mock.call_args_list == [call(foo='bar', baz=123)]


@pytest.mark.asyncio
async def test_call_translates_RPCError(mocker):

    api = MyAPI()
    api.common_rpc_error_map[r'^foo$'] = RuntimeError('bar')

    mocker.patch('aiobtclientrpc.RPCBase.call', side_effect=aiobtclientrpc.RPCError('foo'))
    with pytest.raises(RuntimeError, match=r'^bar$'):
        await api.call()

    mocker.patch('aiobtclientrpc.RPCBase.call', side_effect=aiobtclientrpc.RPCError('asdf'))
    with pytest.raises(aiobtclientrpc.RPCError, match=r'^asdf$'):
        await api.call()


@pytest.mark.parametrize(
    argnames='return_value, exception, exp_result',
    argvalues=(
        ('foo', None, 'foo'),
        (None, aiobtclientrpc.ConnectionError('no net'), errors.ConnectionError('no net: {url}')),
        (None, aiobtclientrpc.TimeoutError('timeout'), errors.TimeoutError('timeout: {url}')),
        (None, aiobtclientrpc.AuthenticationError('bad password'), errors.AuthenticationError('bad password: {url}')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_connect(return_value, exception, exp_result, mocker):
    connect_mock = mocker.patch('aiobtclientrpc.RPCBase.connect', side_effect=exception, return_value=return_value)

    api = MyAPI()
    if isinstance(exp_result, Exception):
        exp_msg = str(exp_result).format(url=api.url)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(exp_msg)}$'):
            await api.connect(foo='bar', baz=123)
    else:
        retval = await api.connect(foo='bar', baz=123)
        assert retval == exp_result

    assert connect_mock.call_args_list == [call(foo='bar', baz=123)]


@pytest.mark.parametrize(
    argnames='return_value, exception, exp_result',
    argvalues=(
        ('foo', None, 'foo'),
        (None, aiobtclientrpc.ConnectionError('no net'), errors.ConnectionError('no net: {url}')),
        (None, aiobtclientrpc.TimeoutError('timeout'), errors.TimeoutError('timeout: {url}')),
        (None, aiobtclientrpc.AuthenticationError('bad password'), errors.AuthenticationError('bad password: {url}')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_disconnect(return_value, exception, exp_result, mocker):
    disconnect_mock = mocker.patch('aiobtclientrpc.RPCBase.disconnect', side_effect=exception, return_value=return_value)

    api = MyAPI()
    if isinstance(exp_result, Exception):
        exp_msg = str(exp_result).format(url=api.url)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(exp_msg)}$'):
            await api.disconnect(foo='bar', baz=123)
    else:
        retval = await api.disconnect(foo='bar', baz=123)
        assert retval == exp_result

    assert disconnect_mock.call_args_list == [call(foo='bar', baz=123)]


def test_normalize_infohash():
    api = MyAPI()
    return_value = api._normalize_infohash('f000000000000000000000000000000000000000')
    assert isinstance(return_value, utils.Infohash)
    assert return_value == 'f000000000000000000000000000000000000000'


@pytest.mark.asyncio
async def test_get_infohashes(mocker):
    infohashes = [
        'f000000000000000000000000000000000000000',  # lower
        'F000000000000000000000000000000000000000',  # upper
        'F00000000000000000000000000000000000000f',  # mixed
    ]

    api = MyAPI()
    mocker.patch.object(api, '_get_infohashes', AsyncMock(return_value=infohashes))
    return_value = await api.get_infohashes()
    assert return_value == infohashes
    for item in return_value:
        assert isinstance(item, utils.Infohash)


@pytest.mark.asyncio
async def test_get_torrent_field(mocker):
    api = MyAPI()
    api._get_torrent_fields.return_value = {'bar': 123, 'baz': 456}
    assert await api._get_torrent_field('f000000000000000000000000000000000000000', 'bar') == 123
    assert api._get_torrent_fields.call_args_list == [
        call('f000000000000000000000000000000000000000', 'bar'),
    ]
    assert await api._get_torrent_field('f000000000000000000000000000000000000000', 'baz') == 456
    assert api._get_torrent_fields.call_args_list == [
        call('f000000000000000000000000000000000000000', 'bar'),
        call('f000000000000000000000000000000000000000', 'baz'),
    ]


@pytest.mark.asyncio
async def test_add(do_method_tests):
    torrents = ('torrent1', 'torrent2', 'torrent3')
    common_kwargs = {
        'location': 'some/path',
        'stopped': Mock(name='mock stopped'),
        'verify': Mock(name='mock verify'),
    }

    await do_method_tests(
        method_name='add',
        method_args=torrents,
        method_kwargs=common_kwargs,
        method_wrapper_name='_add_torrents',
        exp_method_wrapper_kwargs={
            **common_kwargs,
            **{
                'torrents': torrents,
                'location': os.path.abspath(common_kwargs['location']),
            },
        },
        attributes={
            'added': [],
            'already_added': [],
        },
        types={
            'added': utils.Infohash,
            'already_added': utils.Infohash,
        },
        exception_cls=errors.AddTorrentError,
    )


@pytest.mark.asyncio
async def test_add_torrents(do_method_wrapper_tests):
    await do_method_wrapper_tests(
        '_add_torrents', '_add_torrent',
        accepts_arbitrary_kwargs=True,
        takes_infohash=False,
    )


@pytest.mark.asyncio
async def test_start(do_method_tests):
    infohashes = ('f00', '8a5', '8a2')

    await do_method_tests(
        method_name='start',
        method_args=infohashes,
        method_wrapper_name='_start_torrents',
        exp_method_wrapper_args=(infohashes,),
        attributes={
            'started': [],
            'already_started': [],
        },
        types={
            'started': utils.Infohash,
            'already_started': utils.Infohash,
        },
        exception_cls=errors.StartTorrentError,
    )


@pytest.mark.asyncio
async def test_start_torrents(do_method_wrapper_tests):
    await do_method_wrapper_tests(
        '_start_torrents', '_start_torrent',
        accepts_arbitrary_kwargs=False,
        takes_infohash=True,
    )


@pytest.mark.asyncio
async def test_stop(do_method_tests):
    infohashes = ('f00', '8a5', '8a2')

    await do_method_tests(
        method_name='stop',
        method_args=infohashes,
        method_wrapper_name='_stop_torrents',
        exp_method_wrapper_args=(infohashes,),
        attributes={
            'stopped': [],
            'already_stopped': [],
        },
        types={
            'stopped': utils.Infohash,
            'already_stopped': utils.Infohash,
        },
        exception_cls=errors.StopTorrentError,
    )


@pytest.mark.asyncio
async def test_stop_torrents(do_method_wrapper_tests):
    await do_method_wrapper_tests(
        '_stop_torrents', '_stop_torrent',
        accepts_arbitrary_kwargs=False,
        takes_infohash=True,
    )


@pytest.mark.asyncio
async def test_verify(do_method_tests, mocker):
    infohashes = ('f00', '8a5', '8a2')

    await do_method_tests(
        method_name='verify',
        method_args=infohashes,
        method_wrapper_name='_verify_torrents',
        exp_method_wrapper_args=(infohashes,),
        attributes={
            'verifying': [],
            'already_verifying': [],
        },
        types={
            'verifying': utils.Infohash,
            'already_verifying': utils.Infohash,
        },
        exception_cls=errors.VerifyTorrentError,
    )


@pytest.mark.asyncio
async def test_verify_torrents(do_method_wrapper_tests):
    await do_method_wrapper_tests(
        '_verify_torrents', '_verify_torrent',
        accepts_arbitrary_kwargs=False,
        takes_infohash=True,
    )


@pytest.mark.parametrize(
    argnames='infohash, torrent_is_verifying, start_verifying_exception, monitor_result, exp_results',
    argvalues=(
        ('f00', True, None, [], [
            ('already_verifying', 'f00'),
            errors.TorrentAlreadyVerifying('f00'),
        ]),
        ('f00', False, None, [True, True, False], [('verifying', 'f00')]),
        ('f00', False, errors.NoSuchTorrentError('f00'), None, errors.NoSuchTorrentError('f00')),
        ('f00', False, None, errors.TimeoutError('no time left!'), []),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_verify_torrent(infohash, torrent_is_verifying, start_verifying_exception, monitor_result, exp_results, mocker):
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(side_effect=monitor_result),
    ))

    api = MyAPI()
    api._torrent_is_verifying.return_value = torrent_is_verifying
    api._start_verifying.side_effect = start_verifying_exception

    if isinstance(exp_results, BaseException):
        with pytest.raises(type(exp_results), match=rf'^{re.escape(str(exp_results))}$'):
            [yielded async for yielded in api._verify_torrent(infohash)]
    else:
        results = [yielded async for yielded in api._verify_torrent(infohash)]
        assert results == exp_results

    assert api._torrent_is_verifying.call_args_list == [call(infohash)]

    if not torrent_is_verifying:
        assert api._start_verifying.call_args_list == [call(infohash)]
    else:
        assert api._start_verifying.call_args_list == []

    if not torrent_is_verifying and not start_verifying_exception:
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=0.1,
            timeout=1,
        )]
        assert partial_mock.call_args_list == [call(api._torrent_is_verifying, infohash)]
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [call(True)]


@pytest.mark.parametrize(
    argnames='interval, exp_exception',
    argvalues=(
        (None, None),
        (123, None),
        ((1, 2), None),
        ((1, 2, 3), TypeError('Invalid interval: (1, 2, 3)')),
        ('foo', TypeError("Invalid interval: 'foo'")),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_verify_wait(interval, exp_exception, mocker):
    infohashes = ('f00', '8a5', '8a2')

    mocker.patch('aiobtclientapi.clients.base.APIBase._normalize_infohash', side_effect=lambda h: f'normalized:{h}')
    mocker.patch('aiobtclientapi.clients.base.APIBase._verify_wait')
    mocker.patch('aiobtclientapi.utils.merge_async_generators', return_value=AsyncMock(
        __class__=types.AsyncGeneratorType,
        __aiter__=lambda self: self,
        __anext__=AsyncMock(side_effect=(
            [
                AsyncMock(return_value=(infohash, i))()
                for infohash, i in zip(infohashes, range(100))
            ]
            if not exp_exception else None
        )),
    ))

    exp_progresses = [
        (infohashes[0], 0),
        (infohashes[1], 1),
        (infohashes[2], 2),
    ]
    if interval is None:
        exp_interval_min, exp_interval_max = 0.3, 3
    elif isinstance(interval, (int, float)):
        exp_interval_min = exp_interval_max = interval
    elif isinstance(interval, tuple) and len(interval) == 2:
        exp_interval_min, exp_interval_max = interval

    api = MyAPI()
    kwargs = {}
    if interval is not None:
        kwargs['interval'] = interval
    agen = api.verify_wait(*infohashes, **kwargs)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            [(infohash, progress) async for infohash, progress in agen]
    else:
        progresses = [(infohash, progress) async for infohash, progress in agen]
        assert progresses == exp_progresses

        assert api._verify_wait.call_args_list == [
            call('normalized:' + infohashes[i], exp_interval_min, exp_interval_max)
            for i in range(len(exp_progresses))
        ]


@pytest.mark.parametrize(
    argnames=(
        'infohash, torrent_is_verifying_results, get_verifying_progress_results, '
        'exp_yields, exp_exception'
    ),
    argvalues=(
        # Non-Infohash argument
        (
            'f00?',
            [],
            [],
            [],
            AssertionError(''),
        ),
        # Yield until torrent stops verifying
        (
            utils.Infohash('f00000000000000000000000000000000000000f'),
            [True, True, False, 'ignored', 'ignored'],
            [0.123, 17.456],
            [
                (utils.Infohash('f00000000000000000000000000000000000000f'), 0.123),
                (utils.Infohash('f00000000000000000000000000000000000000f'), 'mock interval.progress'),
                (utils.Infohash('f00000000000000000000000000000000000000f'), 17.456),
            ],
            None,
        ),
        # Yield error
        (
            utils.Infohash('f00000000000000000000000000000000000000f'),
            [True, True, errors.Error('no'), 'ignored', 'ignored'],
            [88, 99],
            [
                (utils.Infohash('f00000000000000000000000000000000000000f'), 88),
                (utils.Infohash('f00000000000000000000000000000000000000f'), 'mock interval.progress'),
                (utils.Infohash('f00000000000000000000000000000000000000f'), errors.Error('no')),
            ],
            None,
        ),
        # Yield warning
        (
            utils.Infohash('f00000000000000000000000000000000000000f'),
            [True, True, errors.Warning('huh'), 'ignored', 'ignored'],
            [88, 99],
            [
                (utils.Infohash('f00000000000000000000000000000000000000f'), 88),
                (utils.Infohash('f00000000000000000000000000000000000000f'), 'mock interval.progress'),
                (utils.Infohash('f00000000000000000000000000000000000000f'), errors.Warning('huh')),
            ],
            None,
        ),
        # Raise other exception
        (
            utils.Infohash('f00000000000000000000000000000000000000f'),
            [True, True, RuntimeError('argh'), 'ignored', 'ignored'],
            [88, 99],
            [],
            RuntimeError('argh'),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__verify_wait(infohash, torrent_is_verifying_results, get_verifying_progress_results,
                            exp_yields, exp_exception, mocker):
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    DynamicInterval_mock = mocker.patch(
        'aiobtclientapi.utils.DynamicInterval',
        return_value=Mock(
            sleep=AsyncMock(),
            progress='mock interval.progress',
        ),
    )

    api = MyAPI()

    api._torrent_is_verifying.side_effect = torrent_is_verifying_results
    api._get_verifying_progress.side_effect = get_verifying_progress_results

    agen = api._verify_wait(infohash, 'interval min', 'interval max')
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            [(ih, p) async for ih, p in agen]
    else:
        yields = [(ih, p) async for ih, p in agen]
        assert yields == exp_yields

    if isinstance(exp_exception, AssertionError):
        assert DynamicInterval_mock.call_args_list == []
        assert partial_mock.call_args_list == []
        assert api._torrent_is_verifying.call_args_list == []
    else:
        assert DynamicInterval_mock.call_args_list == [call(
            name=infohash,
            min='interval min',
            max='interval max',
            progress_getter=partial_mock.return_value
        )]

        assert partial_mock.call_args_list == [call(api._get_verifying_progress, infohash)]

        call_count = list(reversed(torrent_is_verifying_results)).index(True)
        assert api._torrent_is_verifying.call_args_list == [call(infohash)] * call_count
