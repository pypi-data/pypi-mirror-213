import base64
import re
from unittest.mock import AsyncMock, Mock, call

import aiobtclientrpc
import pytest

from aiobtclientapi import clients, errors


def test_parent_classes():
    assert issubclass(clients.DelugeAPI, clients.APIBase)
    assert issubclass(clients.DelugeAPI, aiobtclientrpc.RPCBase)
    mro = clients.deluge.DelugeAPI.__mro__
    assert mro.index(clients.base.APIBase) < mro.index(aiobtclientrpc.RPCBase)


@pytest.mark.asyncio
async def test_get_infohashes(mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.call', return_value=['f00', 'b46', 'ba5'])
    api = clients.DelugeAPI()
    infohashes = await api._get_infohashes()
    assert infohashes == ['f00', 'b46', 'ba5']
    assert api.call.call_args_list == [call('core.get_session_state')]


def test_normalize_infohash(mocker):
    parent_mock = mocker.patch('aiobtclientapi.clients.base.APIBase._normalize_infohash')
    api = clients.DelugeAPI()
    infohash = 'F00000000000000000000000000000000000000f'
    return_value = api._normalize_infohash(infohash)
    assert return_value == parent_mock.return_value
    assert parent_mock.call_args_list == [call(infohash.lower())]


@pytest.mark.parametrize(
    argnames='infohash, known_infohashes, fields, response, exp_result',
    argvalues=(
        ('f00f', [], ['foo', 'bar'], None, errors.NoSuchTorrentError('f00f')),
        ('f00f', ['f00f'], ['foo', 'bar'], {'foo': 1}, errors.ValueError("Unknown field: 'bar'")),
        ('f00f', ['f00f'], ['foo', 'bar'], {'bar': 2}, errors.ValueError("Unknown field: 'foo'")),
        ('f00f', ['f00f'], ['foo', 'bar'], {'foo': 1, 'bar': 2, 'baz': 99}, {'foo': 1, 'bar': 2}),
        ('f00f', ['f00f'], ['foo', 'bar'], {}, RuntimeError('Unexpected response: {}')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_torrent_fields(infohash, known_infohashes, fields, response, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.get_infohashes', return_value=known_infohashes)
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.call', return_value=response)
    api = clients.DelugeAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await api._get_torrent_fields(infohash, *fields)
    else:
        return_value = await api._get_torrent_fields(infohash, *fields)
        assert return_value == exp_result
        assert api.call.call_args_list == [call('core.get_torrent_status', infohash, keys=tuple(fields))]


_make_add_torrent_args_stopped_parameters = pytest.mark.parametrize(
    argnames='stopped, exp_stopped_options',
    argvalues=(
        pytest.param(False, {'add_paused': False}, id='started'),
        pytest.param(True, {'add_paused': True}, id='stopped'),
    ),
)
_make_add_torrent_args_verify_parameters = pytest.mark.parametrize(
    argnames='verify, exp_verify_options',
    argvalues=(
        pytest.param(False, {'seed_mode': True}, id='verify'),
        pytest.param(True, {'seed_mode': False}, id='no verify'),
    ),
)
_make_add_torrent_args_location_parameters = pytest.mark.parametrize(
    argnames='location, exp_location_options',
    argvalues=(
        pytest.param(None, {}, id='no location'),
        pytest.param('some/path', {'download_location': 'some/path'}, id='location'),
    ),
)

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_magnet_uri(
        location, exp_location_options,
        verify, exp_verify_options,
        stopped, exp_stopped_options,
        mocker,
):
    api = clients.DelugeAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=True), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'magnet:mock_uri'
    rpc_function, rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_function == 'core.add_torrent_magnet'
    assert rpc_args == {
        'options': {
            **exp_stopped_options,
            **exp_verify_options,
            **exp_location_options,
        },
        'uri': torrent,
    }

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_infohash(
        location, exp_location_options,
        verify, exp_verify_options,
        stopped, exp_stopped_options,
        mocker,
):
    api = clients.DelugeAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=True), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'F00000000000000000000000000000000000000f'
    rpc_function, rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_function == 'core.add_torrent_magnet'
    assert rpc_args == {
        'options': {
            **exp_stopped_options,
            **exp_verify_options,
            **exp_location_options,
        },
        'uri': f'magnet:?xt=urn:btih:{torrent}',
    }

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_url(
        location, exp_location_options,
        verify, exp_verify_options,
        stopped, exp_stopped_options,
        mocker,
):
    api = clients.DelugeAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=True), 'is_url')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', return_value=b'downloaded torrent data'),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )

    torrent = 'http://example.org/torrents/my.torrent'
    rpc_function, rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_function == 'core.add_torrent_file'
    assert rpc_args == {
        'options': {
            **exp_stopped_options,
            **exp_verify_options,
            **exp_location_options,
        },
        'filedump': str(base64.b64encode(mocks.download_bytes.return_value), encoding='ascii'),
        'filename': 'my.torrent',
    }

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.download_bytes(torrent),
    ]

@_make_add_torrent_args_stopped_parameters
@_make_add_torrent_args_verify_parameters
@_make_add_torrent_args_location_parameters
@pytest.mark.asyncio
async def test__make_add_torrent_args_from_file(
        location, exp_location_options,
        verify, exp_verify_options,
        stopped, exp_stopped_options,
        mocker,
):
    api = clients.DelugeAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', return_value=b'read torrent data'),
        'read_bytes',
    )

    torrent = 'path/to/my.torrent'
    rpc_function, rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_function == 'core.add_torrent_file'
    assert rpc_args == {
        'options': {
            **exp_stopped_options,
            **exp_verify_options,
            **exp_location_options,
        },
        'filedump': str(base64.b64encode(mocks.read_bytes.return_value), encoding='ascii'),
        'filename': 'my.torrent',
    }

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.read_bytes(torrent),
    ]


@pytest.mark.parametrize(
    argnames='torrent, call_result, exp_result',
    argvalues=(
        pytest.param(
            'my.torrent',
            'F00f',
            [('added', 'F00f')],
            id='Torrent added',
        ),
        pytest.param(
            'my.torrent',
            aiobtclientrpc.RPCError('Torrent already being added (F00000000000000000000000000000000000000f)'),
            [
                ('already_added', 'F00000000000000000000000000000000000000f'),
                errors.TorrentAlreadyAdded('F00000000000000000000000000000000000000f', name='my.torrent'),
            ],
            id='Torrent already exists ("being added")',
        ),
        pytest.param(
            'my.torrent',
            aiobtclientrpc.RPCError('Torrent already in session (F00000000000000000000000000000000000000f)'),
            [
                ('already_added', 'F00000000000000000000000000000000000000f'),
                errors.TorrentAlreadyAdded('F00000000000000000000000000000000000000f', name='my.torrent'),
            ],
            id='Torrent already exists ("in session")',
        ),
        pytest.param(
            'not.a.torrent.txt',
            aiobtclientrpc.RPCError('Unable to add torrent, decoding filedump failed: yadda yadda'),
            errors.InvalidTorrentError('not.a.torrent.txt'),
            id='Invalid torrent',
        ),
        pytest.param(
            'magnet:invalid_uri',
            aiobtclientrpc.RPCError('Unable to add magnet, invalid magnet info: the_magnet_URI'),
            errors.InvalidTorrentError('magnet:invalid_uri'),
            id='Invalid magnet URI (bad format)',
        ),
        pytest.param(
            'magnet:?xtc=urn:btih:abcdefghijkl',
            aiobtclientrpc.RPCError('non-hexadecimal number found'),
            errors.InvalidTorrentError('magnet:?xtc=urn:btih:abcdefghijkl'),
            id='Invalid magnet URI (non-hex character)',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__add_torrent(torrent, call_result, exp_result, mocker):
    api = clients.DelugeAPI()
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_make_add_torrent_args', return_value=(
            'core.add_my_torrent',
            {'options': {'foo': 'bar'}},
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

    kwargs = {
        'location': 'mock location',
        'stopped': 'mock stopped',
        'verify': 'mock verify',
    }
    exp_rpc_function = mocks._make_add_torrent_args.return_value[0]
    exp_rpc_args = mocks._make_add_torrent_args.return_value[1]

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._add_torrent(torrent, **kwargs)]
    else:
        return_values = [r async for r in api._add_torrent(torrent, **kwargs)]
        assert return_values == exp_result

    assert mocks.mock_calls == [
        call._make_add_torrent_args(torrent=torrent, **kwargs),
        call.call(exp_rpc_function, **exp_rpc_args),
    ]


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        # Torrent is in "Error" state
        (
            'f00f',
            'Error',
            [call('f00f', 'state')],
            [],
            [('errors', 'Cannot start torrent in error state')],
        ),
        # Torrent is already started
        (
            'f00f',
            'not Paused',
            [call('f00f', 'state')],
            [],
            [('already_started', 'f00f'), errors.TorrentAlreadyStarted('f00f')],
        ),
        # Torrent is started
        (
            'f00f',
            'Paused',
            [call('f00f', 'state')],
            [call('core.resume_torrent', 'f00f')],
            [('started', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_start_torrent(infohash, state, exp_call_calls, exp_get_torrent_field_calls, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.call')

    api = clients.DelugeAPI()

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
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [call('Paused', negate=True)]


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        # Torrent is in "Error" state
        (
            'f00f',
            'Error',
            [call('f00f', 'state')],
            [],
            [('errors', 'Cannot stop torrent in error state')],
        ),
        # Torrent is already stopped
        (
            'f00f',
            'Paused',
            [call('f00f', 'state')],
            [],
            [('already_stopped', 'f00f'), errors.TorrentAlreadyStopped('f00f')],
        ),
        # Torrent is stopped
        (
            'f00f',
            'not Paused',
            [call('f00f', 'state')],
            [call('core.pause_torrent', 'f00f')],
            [('stopped', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_stop_torrent(infohash, state, exp_call_calls, exp_get_torrent_field_calls, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.call')

    api = clients.DelugeAPI()

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
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [call('Paused')]


@pytest.mark.asyncio
async def test_start_verifying(mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI.call')
    api = clients.DelugeAPI()
    await api._start_verifying('f00f')
    assert api.call.call_args_list == [call('core.force_recheck', ['f00f'])]


@pytest.mark.parametrize(
    argnames='state, exp_return_value',
    argvalues=(
        ('Checking', True),
        ('not Checking', False),
    ),
)
@pytest.mark.asyncio
async def test_torrent_is_verifying(state, exp_return_value, mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI._get_torrent_field', return_value=state)
    api = clients.DelugeAPI()
    return_value = await api._torrent_is_verifying('f00f')
    assert return_value is exp_return_value
    assert api._get_torrent_field.call_args_list == [call('f00f', 'state')]


@pytest.mark.asyncio
async def test_get_verifying_progress(mocker):
    mocker.patch('aiobtclientapi.clients.deluge.DelugeAPI._get_torrent_field')
    api = clients.DelugeAPI()
    return_value = await api._get_verifying_progress('f00f')
    assert return_value is api._get_torrent_field.return_value
    assert api._get_torrent_field.call_args_list == [call('f00f', 'progress')]
