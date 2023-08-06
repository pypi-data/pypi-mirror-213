import os
import re
import types
from unittest.mock import AsyncMock, Mock, call

import aiobtclientrpc
import pytest

from aiobtclientapi import clients, errors


def test_parent_classes():
    assert issubclass(clients.qbittorrent.QbittorrentAPI, clients.base.APIBase)
    assert issubclass(clients.qbittorrent.QbittorrentAPI, aiobtclientrpc.RPCBase)
    mro = clients.qbittorrent.QbittorrentAPI.__mro__
    assert mro.index(clients.base.APIBase) < mro.index(aiobtclientrpc.RPCBase)


@pytest.mark.asyncio
async def test_get_infohashes(mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.call', return_value=[
        {'hash': 'f00'},
        {'hash': 'b46'},
        {'hash': 'ba5'},
    ])
    api = clients.QbittorrentAPI()
    return_value = await api._get_infohashes()
    assert isinstance(return_value, types.GeneratorType)
    assert list(return_value) == ['f00', 'b46', 'ba5']
    assert api.call.call_args_list == [call('torrents/info')]


@pytest.mark.parametrize(
    argnames='infohash, known_infohashes, fields, response, exp_result',
    argvalues=(
        ('f00f', [], ['name'], None,
         errors.NoSuchTorrentError('f00f')),
        ('f00f', ['f00f'], ['name'], [{'name': 'Foo'}, {'name': 'Bar'}],
         RuntimeError("Unexpected response: [{'name': 'Foo'}, {'name': 'Bar'}]")),
        ('f00f', ['f00f'], ['name', 'asdf'], [{'name': 'Foo'}],
         errors.ValueError("Unknown field: 'asdf'")),
        ('f00f', ['f00f'], ['name', 'state'], [{'name': 'Foo', 'state': 'seeding', 'size': 123}],
         {'name': 'Foo', 'state': 'seeding'}),
        ('f00f', ['f00f'], ['size', 'state'], [{'name': 'Foo', 'state': 'seeding', 'size': 123}],
         {'state': 'seeding', 'size': 123}),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_torrent_fields(infohash, known_infohashes, fields, response, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.get_infohashes', return_value=known_infohashes)
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.call', return_value=response)
    api = clients.QbittorrentAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await api._get_torrent_fields(infohash, *fields)
    else:
        return_value = await api._get_torrent_fields(infohash, *fields)
        assert return_value == exp_result
        assert api.call.call_args_list == [call('torrents/info', hashes=[infohash])]


_make_add_torrent_args_stopped_parameters = pytest.mark.parametrize(
    argnames='stopped, exp_stopped_args',
    argvalues=(
        pytest.param(False, {'paused': 'false'}, id='started'),
        pytest.param(True, {'paused': 'true'}, id='stopped'),
    ),
)
_make_add_torrent_args_verify_parameters = pytest.mark.parametrize(
    argnames='verify, exp_verify_args',
    argvalues=(
        pytest.param(False, {'skip_checking': 'true'}, id='verify'),
        pytest.param(True, {'skip_checking': 'false'}, id='no verify'),
    ),
)
_make_add_torrent_args_location_parameters = pytest.mark.parametrize(
    argnames='location, exp_location_args',
    argvalues=(
        pytest.param(None, {}, id='no location'),
        pytest.param('some/path', {'savepath': 'some/path'}, id='location'),
    ),
)

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_magnet_uri(
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.QbittorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=True), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'magnet:?xt=urn:btih:f000000000000000000000000000000000000000'
    rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{
            'urls': [torrent],
        },
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
    }
    assert infohash == 'f00f'

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.get_infohash(torrent),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_infohash(
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.QbittorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=True), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'F000000000000000000000000000000000000000'
    rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{
            'urls': [f'magnet:?xt=urn:btih:{torrent}'],
        },
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
    }
    assert infohash == 'f00f'

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.get_infohash(torrent),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_url(
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.QbittorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=True), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', return_value=b'downloaded torrent data'),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'http://example.org/torrents/my.torrent'
    rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{
            'files': (
                ('filename', (
                    os.path.basename(torrent),
                    mocks.download_bytes.return_value,
                    'application/x-bittorrent',
                )),
            )
        },
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
    }
    assert infohash == 'f00f'

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.download_bytes(torrent),
        call.get_infohash(mocks.download_bytes.return_value),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_file(
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.QbittorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', return_value=b'read torrent data'),
        'read_bytes',
    )

    torrent = 'path/to/my.torrent'
    rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{
            'files': (
                ('filename', (
                    os.path.basename(torrent),
                    mocks.read_bytes.return_value,
                    'application/x-bittorrent',
                )),
            )
        },
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
    }
    assert infohash == 'f00f'

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.read_bytes(torrent),
        call.get_infohash(mocks.read_bytes.return_value),
    ]


@pytest.mark.parametrize(
    argnames='torrent, call_result, known_infohashes, exp_result',
    argvalues=(
        pytest.param(
            'not.a.torrent.txt',
            aiobtclientrpc.RPCError('not a valid torrent'),
            [],
            errors.InvalidTorrentError('not.a.torrent.txt'),
            id='Invalid torrent (error raised)',
        ),
        pytest.param(
            'my.torrent',
            'Fails.',
            [],
            errors.InvalidTorrentError('my.torrent'),
            id='Invalid torrent (adding failed)',
        ),
        pytest.param(
            'my.torrent',
            'Fails.',
            ['f00f', 'b00b'],
            [
                ('already_added', 'f00f'),
                errors.TorrentAlreadyAdded('f00f', name='my.torrent'),
            ],
            id='Torrent already exists',
        ),
        pytest.param(
            'my.torrent',
            'Ok.',
            [],
            [('added', 'f00f')],
            id='Torrent added',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__add_torrent(torrent, call_result, known_infohashes, exp_result, mocker):
    api = clients.QbittorrentAPI()
    infohash = 'f00f'
    mocker.patch.object(api, 'get_infohashes', return_value=known_infohashes),
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_make_add_torrent_args', return_value=(
            {'rpc': 'args'},
            infohash,
        )),
        '_make_add_torrent_args',
    )
    mocks.attach_mock(
        mocker.patch.object(api, 'call', **(
            {'side_effect': call_result}
            if isinstance(call_result, Exception) else
            {'return_value': call_result}
        )),
        'call',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
            return_value_contains=AsyncMock(),
        )),
        'Monitor',
    )
    mocks.attach_mock(mocks.Monitor.return_value.return_value_contains, 'return_value_contains')

    kwargs = {
        'location': 'mock location',
        'stopped': 'mock stopped',
        'verify': 'mock verify',
    }
    exp_rpc_args = mocks._make_add_torrent_args.return_value[0]
    exp_calls = [
        call._make_add_torrent_args(torrent=torrent, **kwargs),
        call.call('torrents/add', **exp_rpc_args),
    ]

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._add_torrent(torrent, **kwargs)]
    else:
        return_values = [r async for r in api._add_torrent(torrent, **kwargs)]
        assert return_values == exp_result

        if infohash not in known_infohashes:
            exp_calls.append(
                call.Monitor(
                    call=api.get_infohashes,
                    interval=api.monitor_interval,
                    timeout=api._timeout_add_torrent,
                ),
            )
            exp_calls.append(
                call.return_value_contains(infohash),
            )

    assert mocks.mock_calls == exp_calls


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        # Torrent is already started
        (
            'f00f',
            'uploading',
            [call('f00f', 'state')],
            [],
            [('already_started', 'f00f'), errors.TorrentAlreadyStarted('f00f')],
        ),
        # Torrent is started
        (
            'f00f',
            'pausedUP',
            [call('f00f', 'state')],
            [call('torrents/resume', hashes=['f00f'])],
            [('started', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_start_torrent(infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_contains=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.call')

    api = clients.QbittorrentAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._start_torrent(infohash)]
    else:
        result = [r async for r in api._start_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_field.call_args_list == exp_get_torrent_field_calls
    assert api.call.call_args_list == exp_call_calls
    if exp_call_calls:
        assert partial_mock.call_args_list == [call(api._get_torrent_field, infohash, 'state')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_start_torrent,
        )]
        assert Monitor_mock.return_value.return_value_contains.call_args_list == [call('paused', negate=True)]


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        # Torrent is already stopped
        (
            'f00f',
            'pausedUL',
            [call('f00f', 'state')],
            [],
            [('already_stopped', 'f00f'), errors.TorrentAlreadyStopped('f00f')],
        ),
        # Torrent is started
        (
            'f00f',
            'uploading',
            [call('f00f', 'state')],
            [call('torrents/pause', hashes=['f00f'])],
            [('stopped', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_stop_torrent(infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_contains=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.call')

    api = clients.QbittorrentAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._stop_torrent(infohash)]
    else:
        result = [r async for r in api._stop_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_field.call_args_list == exp_get_torrent_field_calls
    assert api.call.call_args_list == exp_call_calls
    if exp_call_calls:
        assert partial_mock.call_args_list == [call(api._get_torrent_field, infohash, 'state')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_stop_torrent,
        )]
        assert Monitor_mock.return_value.return_value_contains.call_args_list == [call('paused')]


@pytest.mark.asyncio
async def test_start_verifying(mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI.call')
    api = clients.QbittorrentAPI()
    await api._start_verifying('f00f')
    assert api.call.call_args_list == [call('torrents/recheck', hashes=['f00f'])]


@pytest.mark.parametrize(
    argnames='state, exp_return_value',
    argvalues=(
        ('checkingUP', True),
        ('checkingDL', True),
        ('checkingFOO', True),
        ('not Checking', False),
    ),
)
@pytest.mark.asyncio
async def test_torrent_is_verifying(state, exp_return_value, mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI._get_torrent_field', return_value=state)
    api = clients.QbittorrentAPI()
    return_value = await api._torrent_is_verifying('f00f')
    assert return_value is exp_return_value
    assert api._get_torrent_field.call_args_list == [call('f00f', 'state')]


@pytest.mark.asyncio
async def test_get_verifying_progress(mocker):
    mocker.patch('aiobtclientapi.clients.qbittorrent.QbittorrentAPI._get_torrent_field', return_value=0.123)
    api = clients.QbittorrentAPI()
    return_value = await api._get_verifying_progress('f00f')
    assert return_value == 12.3
    assert api._get_torrent_field.call_args_list == [call('f00f', 'progress')]
