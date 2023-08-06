import re
from unittest.mock import AsyncMock, Mock, call

import aiobtclientrpc
import pytest

from aiobtclientapi import clients, errors


def test_parent_classes():
    assert issubclass(clients.rtorrent.RtorrentAPI, clients.base.APIBase)
    assert issubclass(clients.rtorrent.RtorrentAPI, aiobtclientrpc.RPCBase)
    mro = clients.rtorrent.RtorrentAPI.__mro__
    assert mro.index(clients.base.APIBase) < mro.index(aiobtclientrpc.RPCBase)


@pytest.mark.asyncio
async def test_get_infohashes(mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.call', return_value=['f00', 'b46', 'ba5'])
    api = clients.RtorrentAPI()
    return_value = await api._get_infohashes()
    assert return_value == ['f00', 'b46', 'ba5']
    assert api.call.call_args_list == [call('download_list')]


@pytest.mark.parametrize(
    argnames='corofunc, infohash, exp_result',
    argvalues=(
        (
            AsyncMock(return_value='foo'),
            'f00f',
            'foo',
        ),
        (
            AsyncMock(side_effect=aiobtclientrpc.RPCError('Could not find info-hash.')),
            None,
            aiobtclientrpc.RPCError('Could not find info-hash.'),
        ),
        (
            AsyncMock(side_effect=aiobtclientrpc.RPCError('Could not find info-hash.')),
            'f00f',
            errors.NoSuchTorrentError('f00f'),
        ),
        (
            AsyncMock(side_effect=aiobtclientrpc.RPCError('Unsupported target type found.')),
            'f00f',
            errors.InvalidTorrentError('f00f'),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_translate_rpc_error(corofunc, infohash, exp_result):
    api = clients.RtorrentAPI()
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await api._translate_rpc_error(corofunc(), infohash)
    else:
        return_value = await api._translate_rpc_error(corofunc(), infohash)
        assert return_value == exp_result


@pytest.mark.asyncio
async def test_get_torrent_fields(mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._translate_rpc_error')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.multicall', Mock())

    api = clients.RtorrentAPI()
    infohash = 'f00f'
    fields = 'foo', 'bar', 'baz'

    return_value = await api._get_torrent_fields(infohash, *fields)
    assert return_value is api._translate_rpc_error.return_value
    assert api._translate_rpc_error.call_args_list == [call(
        api.multicall.return_value,
        infohash=infohash
    )]
    assert api.multicall.call_args_list == [call(
        ('foo', infohash),
        ('bar', infohash),
        ('baz', infohash),
        as_dict=True,
    )]


_make_add_torrent_args_stopped_parameters = pytest.mark.parametrize(
    argnames='stopped, exp_stopped_args',
    argvalues=(
        pytest.param(False, [], id='started'),
        pytest.param(True, [], id='stopped'),
    ),
)
_make_add_torrent_args_verify_parameters = pytest.mark.parametrize(
    argnames='verify, exp_verify_args',
    argvalues=(
        pytest.param(False, [], id='verify'),
        pytest.param(True, [], id='no verify'),
    ),
)
_make_add_torrent_args_location_parameters = pytest.mark.parametrize(
    argnames='location, exp_location_args',
    argvalues=(
        pytest.param(None, [], id='no location'),
        pytest.param('''someone's/path''', [r'''d.directory.set="someone's/path"'''], id='location with single quote'),
        pytest.param('''my/"path"''', [r'''d.directory.set="my/\"path\""'''], id='location with double quote'),
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
    api = clients.RtorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=True), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.read', side_effect=RuntimeError('not used')), 'read')
    mocks.attach_mock(mocker.patch.object(api, 'get_supported_method', side_effect=RuntimeError('not used')), 'get_supported_method')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.clients.rtorrent.utils.add_resume_fields', side_effect=RuntimeError('not used')),
        'add_resume_fields',
    )

    torrent = 'magnet:mock_uri'
    rpc_method, rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_method == 'load.start_verbose'
    assert rpc_args == [
        '', 'magnet:mock_uri',
    ] + (
        exp_location_args
        + exp_verify_args
        + exp_stopped_args
    )
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
    api = clients.RtorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=True), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.read', side_effect=RuntimeError('not used')), 'read')
    mocks.attach_mock(mocker.patch.object(api, 'get_supported_method', side_effect=RuntimeError('not used')), 'get_supported_method')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.clients.rtorrent.utils.add_resume_fields', side_effect=RuntimeError('not used')),
        'add_resume_fields',
    )

    torrent = 'F00000000000000000000000000000000000000f'
    rpc_method, rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_method == 'load.start_verbose'
    assert rpc_args == [
        '', f'magnet:?xt=urn:btih:{torrent}',
    ] + (
        exp_location_args
        + exp_verify_args
        + exp_stopped_args
    )
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
    api = clients.RtorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=True), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.read', return_value=Mock('torrent')), 'read')
    mocks.attach_mock(mocker.patch.object(api, 'get_supported_method', return_value='load.raw_start_verbose'), 'get_supported_method')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', return_value=b'downloaded torrent data'),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', side_effect=RuntimeError('not used')),
        'read_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.clients.rtorrent.utils.add_resume_fields', return_value=b'downloaded torrent data + resume fields'),
        'add_resume_fields',
    )

    torrent = 'http://example.org/torrents/my.torrent'
    rpc_method, rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_method == 'load.raw_start_verbose'
    assert rpc_args == [
        '', (
            b'downloaded torrent data + resume fields'
            if not verify and location else
            b'downloaded torrent data'
        )
    ] + (
        exp_location_args
        + exp_verify_args
        + exp_stopped_args
    )
    assert infohash == 'f00f'

    exp_mock_calls = [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.download_bytes(torrent),
    ]
    if not verify and location:
        exp_mock_calls.extend((
            call.read(b'downloaded torrent data'),
            call.add_resume_fields(mocks.read.return_value, location),
        ))
    exp_mock_calls.extend((
        call.get_supported_method('load.raw_start_verbose', 'load.raw_start'),
        call.get_infohash(
            b'downloaded torrent data + resume fields'
            if not verify and location else
            b'downloaded torrent data'
        ),
    ))
    assert mocks.mock_calls == exp_mock_calls


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
    api = clients.RtorrentAPI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_magnet', return_value=False), 'is_magnet')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_infohash', return_value=False), 'is_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.is_url', return_value=False), 'is_url')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.get_infohash', return_value='f00f'), 'get_infohash')
    mocks.attach_mock(mocker.patch('aiobtclientapi.utils.torrent.read', return_value=Mock('torrent')), 'read')
    mocks.attach_mock(mocker.patch.object(api, 'get_supported_method', return_value='load.raw_start_verbose'), 'get_supported_method')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.download_bytes', side_effect=RuntimeError('not used')),
        'download_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.torrent.read_bytes', return_value=b'read torrent data'),
        'read_bytes',
    )
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.clients.rtorrent.utils.add_resume_fields', return_value=b'read torrent data + resume fields'),
        'add_resume_fields',
    )

    torrent = 'path/to/my.torrent'
    rpc_method, rpc_args, infohash = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_method == 'load.raw_start_verbose'
    assert rpc_args == [
        '', (
            b'read torrent data + resume fields'
            if not verify and location else
            b'read torrent data'
        )
    ] + (
        exp_location_args
        + exp_verify_args
        + exp_stopped_args
    )
    assert infohash == 'f00f'

    exp_mock_calls = [
        call.is_magnet(torrent),
        call.is_infohash(torrent),
        call.is_url(torrent),
        call.read_bytes(torrent),
    ]
    if not verify and location:
        exp_mock_calls.extend((
            call.read(b'read torrent data'),
            call.add_resume_fields(mocks.read.return_value, location),
        ))
    exp_mock_calls.extend((
        call.get_supported_method('load.raw_start_verbose', 'load.raw_start'),
        call.get_infohash(
            b'read torrent data + resume fields'
            if not verify and location else
            b'read torrent data'
        ),
    ))
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='torrent, location, stopped, verify, rpc_method, rpc_args, infohash, known_infohashes, exp_results, exp_mock_calls',
    argvalues=(
        pytest.param(
            'my.torrent', 'my/location', 'maybe stopped', 'maybe verify',
            'rpc.method', ('rpc', 'args'), 'f00',
            ('f00', 'b00', 'b44'),
            [
                ('already_added', 'f00'),
                errors.TorrentAlreadyAdded('f00', 'my.torrent'),
            ],
            [
                call._make_add_torrent_args(torrent='my.torrent', location='my/location', stopped='maybe stopped', verify='maybe verify'),
                call.get_infohashes(),
            ],
            id='Torrent already added',
        ),
        pytest.param(
            'my.torrent', 'my/location', False, False,
            'rpc.method', ('rpc', 'args'), 'f00',
            ('b00', 'b44'),
            [
                ('added', 'f00'),
            ],
            [
                call._make_add_torrent_args(torrent='my.torrent', location='my/location', stopped=False, verify=False),
                call.get_infohashes(),
                call.call('rpc.method', 'rpc', 'args'),
                'placeholder:call.Monitor',
            ],
            id='Torrent added (stopped=False, verify=False)',
        ),
        pytest.param(
            'my.torrent', 'my/location', False, True,
            'rpc.method', ('rpc', 'args'), 'f00',
            ('b00', 'b44'),
            [
                ('added', 'f00'),
            ],
            [
                call._make_add_torrent_args(torrent='my.torrent', location='my/location', stopped=False, verify=True),
                call.get_infohashes(),
                call.call('rpc.method', 'rpc', 'args'),
                'placeholder:call.Monitor',
            ],
            id='Torrent added (stopped=False, verify=True)',
        ),
        pytest.param(
            'my.torrent', 'my/location', True, False,
            'rpc.method', ('rpc', 'args'), 'f00',
            ('b00', 'b44'),
            [
                ('added', 'f00'),
                'stop response',
            ],
            [
                call._make_add_torrent_args(torrent='my.torrent', location='my/location', stopped=True, verify=False),
                call.get_infohashes(),
                call.call('rpc.method', 'rpc', 'args'),
                'placeholder:call.Monitor',
                call.stop('f00'),
            ],
            id='Torrent added (stopped=True, verify=False)',
        ),
        pytest.param(
            'my.torrent', 'my/location', True, True,
            'rpc.method', ('rpc', 'args'), 'f00',
            ('b00', 'b44'),
            [
                ('added', 'f00'),
                'stop response',
                'verify response',
            ],
            [
                call._make_add_torrent_args(torrent='my.torrent', location='my/location', stopped=True, verify=True),
                call.get_infohashes(),
                call.call('rpc.method', 'rpc', 'args'),
                'placeholder:call.Monitor',
                call.stop('f00'),
                call.verify('f00'),
            ],
            id='Torrent added (stopped=True, verify=True)',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__add_torrent(torrent, location, stopped, verify,
                            rpc_method, rpc_args, infohash,
                            known_infohashes,
                            exp_results, exp_mock_calls, mocker):
    api = clients.RtorrentAPI()

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_make_add_torrent_args', return_value=(rpc_method, rpc_args, infohash)),
        '_make_add_torrent_args',
    )
    mocks.attach_mock(
        mocker.patch.object(api, 'get_infohashes', return_value=known_infohashes),
        'get_infohashes',
    )
    mocks.attach_mock(mocker.patch.object(api, 'call'), 'call')
    mocks.attach_mock(
        mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
            return_value_contains=AsyncMock(),
        )),
        'Monitor',
    )
    mocks.attach_mock(mocks.Monitor.return_value_contains, 'return_value_contains')
    mocks.attach_mock(mocker.patch.object(api, 'stop', return_value='stop response'), 'stop')
    mocks.attach_mock(mocker.patch.object(api, 'verify', return_value='verify response'), 'verify')

    agen = api._add_torrent(
        torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    if isinstance(exp_results, Exception):
        with pytest.raises(type(exp_results), match=rf'^{re.escape(str(exp_results))}$'):
            [r async for r in agen]
    else:
        return_values = [r async for r in agen]
        assert return_values == exp_results

    if 'placeholder:call.Monitor' in exp_mock_calls:
        exp_mock_calls[exp_mock_calls.index('placeholder:call.Monitor')] = call.Monitor(
            call=api.get_infohashes,
            interval=api.monitor_interval,
            timeout=api._timeout_add_torrent,
        )

    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_fields_calls, exp_success, exp_result',
    argvalues=(
        # Torrent is already started
        (
            'f00f',
            {'d.is_open': 1, 'd.is_active': 1},
            [call('f00f', 'd.is_open', 'd.is_active')],
            False,
            [('already_started', 'f00f'), errors.TorrentAlreadyStarted('f00f')],
        ),
        # Torrent is started
        (
            'f00f',
            {'d.is_open': 0, 'd.is_active': 0},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('started', 'f00f')],
        ),
        (
            'f00f',
            {'d.is_open': 0, 'd.is_active': 1},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('started', 'f00f')],
        ),
        (
            'f00f',
            {'d.is_open': 1, 'd.is_active': 0},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('started', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_start_torrent(infohash, state, exp_get_torrent_fields_calls, exp_success, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._get_torrent_fields', return_value=state)
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._translate_rpc_error')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.multicall', Mock())
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.call')

    api = clients.RtorrentAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._start_torrent(infohash)]
    else:
        result = [r async for r in api._start_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_fields.call_args_list == exp_get_torrent_fields_calls
    if exp_success:
        assert api.multicall.call_args_list == [call(
            ('d.open', infohash),
            ('d.start', infohash),
        )]
        assert api._translate_rpc_error.call_args_list == [call(
            api.multicall.return_value,
            infohash=infohash,
        )]
        assert partial_mock.call_args_list == [call(api._get_torrent_fields, infohash, 'd.is_open', 'd.is_active')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_start_torrent,
        )]
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [call({'d.is_open': 1, 'd.is_active': 1})]
    else:
        assert api.multicall.call_args_list == []
        assert api._translate_rpc_error.call_args_list == []
        assert partial_mock.call_args_list == []
        assert Monitor_mock.call_args_list == []
        assert Monitor_mock.return_value.return_value_equals.call_args_list == []


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_fields_calls, exp_success, exp_result',
    argvalues=(
        # Torrent is already stopped
        (
            'f00f',
            {'d.is_open': 0, 'd.is_active': 0},
            [call('f00f', 'd.is_open', 'd.is_active')],
            False,
            [('already_stopped', 'f00f'), errors.TorrentAlreadyStopped('f00f')],
        ),
        (
            'f00f',
            {'d.is_open': 0, 'd.is_active': 1},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('stopped', 'f00f')],
        ),
        (
            'f00f',
            {'d.is_open': 1, 'd.is_active': 0},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('stopped', 'f00f')],
        ),
        # Torrent is started
        (
            'f00f',
            {'d.is_open': 1, 'd.is_active': 1},
            [call('f00f', 'd.is_open', 'd.is_active')],
            True,
            [('stopped', 'f00f')],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_stop_torrent(infohash, state, exp_get_torrent_fields_calls, exp_success, exp_result, mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._get_torrent_fields', return_value=state)
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._translate_rpc_error')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.multicall', Mock())
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.call')

    api = clients.RtorrentAPI()

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._stop_torrent(infohash)]
    else:
        result = [r async for r in api._stop_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_fields.call_args_list == exp_get_torrent_fields_calls
    if exp_success:
        assert api.multicall.call_args_list == [call(
            ('d.stop', infohash),
            ('d.close', infohash),
        )]
        assert api._translate_rpc_error.call_args_list == [call(
            api.multicall.return_value,
            infohash=infohash,
        )]
        assert partial_mock.call_args_list == [call(api._get_torrent_fields, infohash, 'd.is_open', 'd.is_active')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_stop_torrent,
        )]
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [call({'d.is_open': 0, 'd.is_active': 0})]
    else:
        assert api.multicall.call_args_list == []
        assert api._translate_rpc_error.call_args_list == []
        assert partial_mock.call_args_list == []
        assert Monitor_mock.call_args_list == []
        assert Monitor_mock.return_value.return_value_equals.call_args_list == []


@pytest.mark.asyncio
async def test_start_verifying(mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._translate_rpc_error')
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI.call', Mock())

    api = clients.RtorrentAPI()

    await api._start_verifying('f00f')
    assert api.call.call_args_list == [call('d.check_hash', 'f00f')]
    assert api._translate_rpc_error.call_args_list == [call(
        api.call.return_value,
        infohash='f00f',
    )]


@pytest.mark.parametrize(
    argnames='hashing, exp_return_value',
    argvalues=(
        (0, False),
        (1, True),
        (2, True),
        (3, True),
    ),
)
@pytest.mark.asyncio
async def test_torrent_is_verifying(hashing, exp_return_value, mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._get_torrent_field', return_value=hashing)

    api = clients.RtorrentAPI()

    return_value = await api._torrent_is_verifying('f00f')
    assert return_value is exp_return_value
    assert api._get_torrent_field.call_args_list == [call('f00f', 'd.hashing')]


@pytest.mark.asyncio
async def test_get_verifying_progress(mocker):
    mocker.patch('aiobtclientapi.clients.rtorrent.RtorrentAPI._get_torrent_fields', return_value={
        'd.chunks_hashed': 9,
        'd.size_chunks': 36,
    })
    api = clients.RtorrentAPI()
    return_value = await api._get_verifying_progress('f00f')
    assert return_value == 25
    assert api._get_torrent_fields.call_args_list == [call('f00f', 'd.chunks_hashed', 'd.size_chunks')]
