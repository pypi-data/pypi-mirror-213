import base64
import re
import types
from unittest.mock import AsyncMock, Mock, call

import aiobtclientrpc
import pytest

from aiobtclientapi import clients, errors
from aiobtclientapi.clients.transmission import enums


@pytest.fixture
def api():
    return clients.TransmissionAPI()


def test_parent_classes():
    assert issubclass(clients.transmission.TransmissionAPI, clients.base.APIBase)
    assert issubclass(clients.transmission.TransmissionAPI, aiobtclientrpc.RPCBase)
    mro = clients.transmission.TransmissionAPI.__mro__
    assert mro.index(clients.base.APIBase) < mro.index(aiobtclientrpc.RPCBase)


@pytest.mark.asyncio
async def test_get_infohashes(api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI.call', return_value={
        'arguments': {
            'torrents': [
                {'hashString': 'f00'},
                {'hashString': 'b46'},
                {'hashString': 'ba5'},
            ],
        },
    })
    return_value = await api._get_infohashes()
    assert isinstance(return_value, types.GeneratorType)
    assert list(return_value) == ['f00', 'b46', 'ba5']
    assert api.call.call_args_list == [call('torrent-get', fields=['hashString'])]


@pytest.mark.parametrize(
    argnames='infohash, fields, response, exp_result',
    argvalues=(
        ('f00f', ['foo', 'bar'], {'arguments': {'torrents': []}},
         errors.NoSuchTorrentError('f00f')),
        ('f00f', ['foo', 'bar'], {'arguments': {'torrents': [{'foo': 1, 'bar': 2, 'baz': 9}]}},
         {'foo': 1, 'bar': 2}),
        ('f00f', ['foo', 'ASDF'], {'arguments': {'torrents': [{'foo': 1, 'bar': 2}]}},
         errors.ValueError("Unknown field: 'ASDF'")),
        ('f00f', ['foo', 'ASDF'], {'arguments': {'torrents': [{'foo': 1}, {'foo': 2}]}},
         RuntimeError("Unexpected torrent list: [{'foo': 1}, {'foo': 2}]")),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_torrent_fields(infohash, fields, response, exp_result, api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI.call', return_value=response)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await api._get_torrent_fields(infohash, *fields)
    else:
        return_value = await api._get_torrent_fields(infohash, *fields)
        assert return_value == exp_result
        assert api.call.call_args_list == [call('torrent-get', ids=[infohash], fields=tuple(fields))]


@pytest.mark.parametrize(
    argnames='kwargs, exp_warnings',
    argvalues=(
        (
            {},
            [],
        ),
        (
            {'verify': True},
            [],
        ),
        (
            {'verify': False},
            [
                errors.Warning(f'Adding torrents without verification is not supported by {clients.TransmissionAPI.label}'),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__add_torrents(kwargs, exp_warnings, api, mocker):
    parent_return_values = ['a', 'b', 'c']
    parent_mock = mocker.patch('aiobtclientapi.clients.base.APIBase._add_torrents', return_value=AsyncMock(
        __class__=types.AsyncGeneratorType,
        __aiter__=lambda self: self,
        __anext__=AsyncMock(side_effect=parent_return_values),
    ))

    torrents = ('foo',)
    return_values = [r async for r in api._add_torrents(torrents, **kwargs)]
    assert return_values == exp_warnings + parent_return_values
    assert parent_mock.call_args_list == [call(torrents, **kwargs)]


_make_add_torrent_args_stopped_parameters = pytest.mark.parametrize(
    argnames='stopped, exp_stopped_args',
    argvalues=(
        pytest.param(False, {'paused': False}, id='started'),
        pytest.param(True, {'paused': True}, id='stopped'),
    ),
)
_make_add_torrent_args_verify_parameters = pytest.mark.parametrize(
    argnames='verify, exp_verify_args',
    argvalues=(
        pytest.param(False, {}, id='verify'),
        pytest.param(True, {}, id='no verify'),
    ),
)
_make_add_torrent_args_location_parameters = pytest.mark.parametrize(
    argnames='location, exp_location_args',
    argvalues=(
        pytest.param(None, {}, id='no location'),
        pytest.param('some/path', {'download-dir': 'some/path'}, id='location'),
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
    api = clients.TransmissionAPI()
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
    rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{'filename': torrent},
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
    }

    assert mocks.mock_calls == [
        call.is_magnet(torrent),
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
    api = clients.TransmissionAPI()
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

    torrent = 'F000000000000000000000000000000000000000'
    rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{'filename': f'magnet:?xt=urn:btih:{torrent}'},
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
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
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.TransmissionAPI()
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

    torrent = 'F000000000000000000000000000000000000000'
    rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{'metainfo': str(base64.b64encode(b'downloaded torrent data'), encoding='ascii')},
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
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
        location, exp_location_args,
        verify, exp_verify_args,
        stopped, exp_stopped_args,
        mocker,
):
    api = clients.TransmissionAPI()
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
    rpc_args = await api._make_add_torrent_args(
        torrent=torrent,
        location=location,
        stopped=stopped,
        verify=verify,
    )
    assert rpc_args == {
        **{'metainfo': str(base64.b64encode(b'read torrent data'), encoding='ascii')},
        **exp_stopped_args,
        **exp_verify_args,
        **exp_location_args,
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
            aiobtclientrpc.RPCError('Duplicate torrent', info={'torrent-duplicate': {'hashString': 'F00f'}}),
            [
                ('already_added', 'F00f'),
                errors.TorrentAlreadyAdded('F00f', name='my.torrent'),
            ],
            id='Torrent already exists (Transmission 4.0.{0,1,2})',
        ),
        pytest.param(
            'my.torrent',
            aiobtclientrpc.RPCError('Unrecognized info', info={'more': 'info'}),
            errors.InvalidTorrentError('my.torrent'),
            id='Invalid torrent (Transmission 4.*)',
        ),
        pytest.param(
            'my.torrent',
            aiobtclientrpc.RPCError('Invalid or corrupt torrent file', info={'more': 'info'}),
            errors.InvalidTorrentError('my.torrent'),
            id='Invalid torrent (Transmission 3.*)',
        ),
        pytest.param(
            'my.torrent',
            {'result': 'success', 'arguments': {'torrent-duplicate': {'hashString': 'F00f'}}},
            [
                ('already_added', 'F00f'),
                errors.TorrentAlreadyAdded('F00f', name='my.torrent'),
            ],
            id='Torrent already exists (Transmission 3.*,>=4.0.3)',
        ),
        pytest.param(
            'my.torrent',
            {'result': 'success', 'arguments': {'torrent-added': {'hashString': 'F00f'}}},
            [('added', 'F00f')],
            id='Torrent added',
        ),
        pytest.param(
            'my.torrent',
            {'result': 'success', 'arguments': {'torrent-bedazzled': {'hashString': 'F00f'}}},
            RuntimeError("Unexpected response: {'result': 'success', 'arguments': {'torrent-bedazzled': {'hashString': 'F00f'}}}"),
            id='Unexpected response',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__add_torrent(torrent, call_result, exp_result, mocker):
    api = clients.TransmissionAPI()
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_make_add_torrent_args', return_value={'foo': 'bar'}),
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
    exp_rpc_function = 'torrent-add'
    exp_rpc_args = mocks._make_add_torrent_args.return_value

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._add_torrent(torrent, **kwargs)]
    else:
        return_values = [r async for r in api._add_torrent(torrent, **kwargs)]
        assert return_values == exp_result

    assert mocks.mock_calls == [
        call._make_add_torrent_args(torrent=torrent, **kwargs),
        call.call(exp_rpc_function, exp_rpc_args),
    ]


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        pytest.param(
            'f00f',
            enums.TR_STATUS.DOWNLOAD,
            [call('f00f', 'status')],
            [],
            [('already_started', 'f00f'), errors.TorrentAlreadyStarted('f00f')],
            id='Torrent is already started (downloading)',
        ),
        pytest.param(
            'f00f',
            enums.TR_STATUS.SEED,
            [call('f00f', 'status')],
            [],
            [('already_started', 'f00f'), errors.TorrentAlreadyStarted('f00f')],
            id='Torrent is already started (seeding)',
        ),
        pytest.param(
            'f00f',
            enums.TR_STATUS.STOPPED,
            [call('f00f', 'status')],
            [call('torrent-start', ids=['f00f'])],
            [('started', 'f00f')],
            id='Torrent is started',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_start_torrent(infohash, state, exp_call_calls, exp_get_torrent_field_calls, exp_result, api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI.call')

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._start_torrent(infohash)]
    else:
        result = [r async for r in api._start_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_field.call_args_list == exp_get_torrent_field_calls
    assert api.call.call_args_list == exp_call_calls
    if exp_call_calls:
        assert partial_mock.call_args_list == [call(api._get_torrent_field, infohash, 'status')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_start_torrent,
        )]
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [
            call(enums.TR_STATUS.STOPPED, negate=True),
        ]


@pytest.mark.parametrize(
    argnames='infohash, state, exp_get_torrent_field_calls, exp_call_calls, exp_result',
    argvalues=(
        pytest.param(
            'f00f',
            enums.TR_STATUS.STOPPED,
            [call('f00f', 'status')],
            [],
            [('already_stopped', 'f00f'), errors.TorrentAlreadyStopped('f00f')],
            id='Torrent is already stopped',
        ),
        pytest.param(
            'f00f',
            enums.TR_STATUS.DOWNLOAD,
            [call('f00f', 'status')],
            [call('torrent-stop', ids=['f00f'])],
            [('stopped', 'f00f')],
            id='Torrent is stopped (downloading)',
        ),
        pytest.param(
            'f00f',
            enums.TR_STATUS.SEED,
            [call('f00f', 'status')],
            [call('torrent-stop', ids=['f00f'])],
            [('stopped', 'f00f')],
            id='Torrent is stopped (seeding)',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_stop_torrent(infohash, state, exp_call_calls, exp_get_torrent_field_calls, exp_result, api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI._get_torrent_field', return_value=state)
    Monitor_mock = mocker.patch('aiobtclientapi.utils.Monitor', return_value=Mock(
        return_value_equals=AsyncMock(),
    ))
    partial_mock = mocker.patch('aiobtclientapi.utils.partial')
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI.call')

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            [r async for r in api._stop_torrent(infohash)]
    else:
        result = [r async for r in api._stop_torrent(infohash)]
        assert result == exp_result

    assert api._get_torrent_field.call_args_list == exp_get_torrent_field_calls
    assert api.call.call_args_list == exp_call_calls
    if exp_call_calls:
        assert partial_mock.call_args_list == [call(api._get_torrent_field, infohash, 'status')]
        assert Monitor_mock.call_args_list == [call(
            call=partial_mock.return_value,
            interval=api.monitor_interval,
            timeout=api._timeout_stop_torrent,
        )]
        assert Monitor_mock.return_value.return_value_equals.call_args_list == [
            call(enums.TR_STATUS.STOPPED),
        ]


@pytest.mark.asyncio
async def test_start_verifying(api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI.call')
    await api._start_verifying('f00f')
    assert api.call.call_args_list == [call('torrent-verify', ids=['f00f'])]


@pytest.mark.parametrize(
    argnames='status, exp_return_value',
    argvalues=(
        (enums.TR_STATUS.STOPPED, False),
        (enums.TR_STATUS.CHECK_WAIT, True),
        (enums.TR_STATUS.CHECK, True),
        (enums.TR_STATUS.DOWNLOAD_WAIT, False),
        (enums.TR_STATUS.DOWNLOAD, False),
        (enums.TR_STATUS.SEED_WAIT, False),
        (enums.TR_STATUS.SEED, False),
    ),
)
@pytest.mark.asyncio
async def test_torrent_is_verifying(status, exp_return_value, api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI._get_torrent_field', return_value=status)
    return_value = await api._torrent_is_verifying('f00f')
    assert return_value is exp_return_value
    assert api._get_torrent_field.call_args_list == [call('f00f', 'status')]


@pytest.mark.parametrize(
    argnames='response, exp_return_value',
    argvalues=(
        ({'status': enums.TR_STATUS.CHECK, 'recheckProgress': 0, 'percentDone': 0.123}, 0),
        ({'status': enums.TR_STATUS.CHECK, 'recheckProgress': 0.123, 'percentDone': 0.456}, 12.3),
        ({'status': enums.TR_STATUS.CHECK_WAIT, 'recheckProgress': 0, 'percentDone': 0.123}, 0),
        ({'status': enums.TR_STATUS.CHECK_WAIT, 'recheckProgress': 0.123, 'percentDone': 0.456}, 12.3),
        ({'status': enums.TR_STATUS.STOPPED, 'recheckProgress': 0, 'percentDone': 0.123}, 12.3),
        ({'status': enums.TR_STATUS.DOWNLOAD_WAIT, 'recheckProgress': 0, 'percentDone': 0.123}, 12.3),
        ({'status': enums.TR_STATUS.DOWNLOAD, 'recheckProgress': 0, 'percentDone': 0.123}, 12.3),
        ({'status': enums.TR_STATUS.SEED_WAIT, 'recheckProgress': 0, 'percentDone': 0.123}, 12.3),
        ({'status': enums.TR_STATUS.SEED, 'recheckProgress': 0, 'percentDone': 0.123}, 12.3),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_verifying_progress(response, exp_return_value, api, mocker):
    mocker.patch('aiobtclientapi.clients.transmission.TransmissionAPI._get_torrent_fields', return_value=response)

    return_value = await api._get_verifying_progress('f00f')
    assert return_value == exp_return_value
    assert api._get_torrent_fields.call_args_list == [call('f00f', 'status', 'recheckProgress', 'percentDone')]

    async def _get_verifying_progress(self, infohash):
        torrent = await self._get_torrent_fields(infohash, 'status', 'recheckProgress', 'percentDone')
        if torrent['status'] in (enums.TR_STATUS.CHECK, enums.TR_STATUS.CHECK_WAIT):
            return torrent['recheckProgress'] * 100
        else:
            # NOTE: Despite the name, "percentDone" is also a fraction from 0 to 1.
            return torrent['percentDone'] * 100
