import errno
import io
import re
from unittest.mock import AsyncMock, Mock, call, mock_open

import httpx
import pytest

from aiobtclientapi import constants, errors, utils


@pytest.mark.parametrize(
    argnames='value, exp_return_value',
    argvalues=(
        ('magnet:arfarfarf', True),
        ('Magnet:arfarfarf', True),
        ('MAGNET:arfarfarf', True),
        ('magneturi:arfarfarf', False),
        ('themagnet:arfarfarf', False),
        (None, False),
        (123, False),
        ('', False),
    ),
    ids=lambda v: repr(v),
)
def test_is_magnet(value, exp_return_value):
    assert utils.is_magnet(value) is exp_return_value


@pytest.mark.parametrize(
    argnames='value, exp_return_value',
    argvalues=(
        ('0123456789abcdef0123456789abcdef01234567', True),
        ('0123456789ABCDEF0123456789ABCDEF01234567', True),
        ('0123456789ABCDEF0123456789abcdeF01234567', True),
        ('0123456789ABCDEF0123456789abcdeF0123456x', False),
        (123456789012345678901234567890123456789, False),    # 39 digits
        (1234567890123456789012345678901234567890, True),    # 40 digits
        (12345678901234567890123456789012345678901, False),  # 41 digits
        (None, False),
        (123, False),
        ('', False),
    ),
    ids=lambda v: repr(v),
)
def test_is_infohash(value, exp_return_value):
    assert utils.is_infohash(value) is exp_return_value


@pytest.mark.parametrize(
    argnames='value, exp_result',
    argvalues=(
        ('0123456789abcdef0123456789abcdef01234567', '0123456789abcdef0123456789abcdef01234567'),
        ('0123456789ABCDEF0123456789ABCDEF01234567', '0123456789abcdef0123456789abcdef01234567'),
        ('0123456789ABCDEF0123456789abcdeF01234567', '0123456789abcdef0123456789abcdef01234567'),
        ('0123456789ABCDEF0123456789abcdeF0123456x', ValueError("Invalid infohash: '0123456789ABCDEF0123456789abcdeF0123456x'")),
        ('0123456789ABCDEF0123456789abcdeF0123456x', ValueError("Invalid infohash: '0123456789ABCDEF0123456789abcdeF0123456x'")),
        (None, ValueError('Invalid infohash: None')),
    ),
    ids=lambda v: repr(v),
)
def test_Infohash(value, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            utils.Infohash(value)
    else:
        result = utils.Infohash(value)
        assert result == exp_result
        assert str(result) == str(result).lower()


@pytest.mark.parametrize(
    argnames='infohash, other, exp_return_value',
    argvalues=(
        (utils.Infohash('0123456789abcdef0123456789abcdef01234567'), '0123456789abcdef0123456789abcdef01234568', False),
        (utils.Infohash('0123456789abcdef0123456789abcdef01234567'), '0123456789abcdef0123456789abcdef012345677', False),
        (utils.Infohash('0123456789abcdef0123456789abcdef01234567'), '0123456789abcdef0123456789abcdef01234567', True),
        (utils.Infohash('0123456789abcdef0123456789abcdef01234567'), '0123456789ABCDEF0123456789abcdef01234567', True),
        (utils.Infohash('0123456789abcdef0123456789ABCDEF01234567'), '0123456789abcdef0123456789ABCDEF01234567', True),
        (utils.Infohash('0123456789abcdef0123456789ABCDEF01234567'), '0123456789abcdef0123456789ABCDEF01234567', True),
        (utils.Infohash('0123456789abcdef0123456789ABCDEF01234567'), 123, NotImplemented),
    ),
    ids=lambda v: repr(v),
)
def test_Infohash_equality(infohash, other, exp_return_value):
    assert infohash.__eq__(other) is exp_return_value


@pytest.mark.parametrize(
    argnames='value, exp_return_value',
    argvalues=(
        ('http://foo', True),
        ('Http://foo', True),
        ('HTTPS://foo', True),
        ('FiLe:///foo', True),
        ('h/t.t,p:///foo', False),
        (None, False),
        (123, False),
        ('', False),
    ),
    ids=lambda v: repr(v),
)
def test_is_url(value, exp_return_value):
    assert utils.is_url(value) is exp_return_value


@pytest.mark.parametrize(
    argnames='size, maxsize, exp_exception',
    argvalues=(
        (5000, None, None),
        (5000, 5000, None),
        (5001, 5000, errors.ReadError('Too big (5001 bytes): {filepath}')),
    ),
    ids=lambda v: repr(v),
)
def test_read_bytes_with_maxsize(size, maxsize, exp_exception, tmp_path):
    filepath = tmp_path / 'foo'
    content = b'x' * size
    filepath.write_bytes(content)

    if exp_exception:
        exp_msg = str(exp_exception).format(filepath=filepath)
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
            utils.read_bytes(filepath, maxsize=maxsize)
    else:
        assert utils.read_bytes(filepath, maxsize=maxsize) == content


@pytest.mark.parametrize(
    argnames='exception, exp_exception',
    argvalues=(
        (OSError('no'), errors.ReadError('no: {filepath}')),
        (OSError(errno.EACCES, 'Permission denied'), errors.ReadError('Permission denied: {filepath}')),
    ),
    ids=lambda v: repr(v),
)
def test_read_bytes_captures_OSError_from_getsize(exception, exp_exception, tmp_path, mocker):
    filepath = tmp_path / 'foo'
    content = b'x' * 100
    filepath.write_bytes(content)

    mocker.patch('os.path.getsize', side_effect=exception)

    exp_msg = str(exp_exception).format(filepath=filepath)
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
        utils.read_bytes(filepath, maxsize=999)


def test_read_bytes_captures_OSError_from_open():
    filepath = '/no/such/path'
    with pytest.raises(errors.ReadError, match=r'^No such file or directory: /no/such/path$'):
        utils.read_bytes(filepath, maxsize=999)


@pytest.mark.parametrize(
    argnames='exception, exp_exception',
    argvalues=(
        (OSError('no'), errors.ReadError('no: {filepath}')),
        (OSError(errno.EACCES, 'Permission denied'), errors.ReadError('Permission denied: {filepath}')),
    ),
    ids=lambda v: repr(v),
)
def test_read_bytes_captures_OSError_from_reading(exception, exp_exception, mocker, tmp_path):
    filepath = tmp_path / 'foo'
    mocker.patch('os.path.getsize', return_value=123)

    mocked_open = mocker.patch('builtins.open', mock_open())
    mocked_open.return_value.read = Mock(side_effect=exception)

    exp_msg = str(exp_exception).format(filepath=filepath)
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
        utils.read_bytes(filepath, maxsize=999)


@pytest.mark.parametrize(
    argnames='exception, exp_exception',
    argvalues=(
        (OSError('no'), errors.WriteError('no: {filepath}')),
        (OSError(errno.EACCES, 'Permission denied'), errors.WriteError('Permission denied: {filepath}')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_download_captures_OSError_from_opening_target(exception, exp_exception, mocker, tmp_path):
    url = 'http://localhost:12345/file/to/download.jpg'
    filepath = tmp_path / 'foo'

    mocked_open = mocker.patch('builtins.open', mock_open())
    mocked_open.side_effect = exception

    exp_msg = str(exp_exception).format(filepath=filepath)
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
        await utils.download(url, to=filepath)


@pytest.mark.parametrize(
    argnames='to',
    argvalues=(
        None,
        '',
        '/some/path',
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_download_calls_download_to_stream(to, mocker, tmp_path):
    url = 'http://localhost:12345/file/to/download.jpg'

    mocked_open = mocker.patch('builtins.open', mock_open())
    BytesIO_mock = mocker.patch('io.BytesIO')
    download_to_stream_mock = mocker.patch('aiobtclientapi.utils._download_to_stream')

    return_value = await utils.download(url, to=to, maxsize=123)
    if to:
        assert download_to_stream_mock.call_args_list == [call(url, mocked_open.return_value, 123)]
        assert mocked_open.call_args_list == [call(to, 'wb')]
        assert return_value is None
    else:
        assert download_to_stream_mock.call_args_list == [call(url, BytesIO_mock.return_value, 123)]
        assert BytesIO_mock.return_value.seek.call_args_list == [call(0)]
        assert return_value is BytesIO_mock.return_value.read.return_value


@pytest.mark.parametrize(
    argnames='exception, exp_exception, to',
    argvalues=(
        (
            httpx.HTTPStatusError(
                'asdf',
                request=None,
                response=Mock(reason_phrase='Not found'),
            ),
            errors.ReadError('Not found: http://localhost:12345'),
            None,
        ),
        (
            httpx.TimeoutException('timeout'),
            errors.ReadError(f'Timeout after {constants.HTTP_REQUEST_TIMEOUT} seconds: http://localhost:12345'),
            None,
        ),
        (
            httpx.HTTPError('Generic error'),
            errors.ReadError('Generic error: http://localhost:12345'),
            None,
        ),
        (
            OSError('No'),
            errors.WriteError('No'),
            None,
        ),
        (
            OSError(errno.ENOMEM, 'No memory left'),
            errors.WriteError('No memory left'),
            None,
        ),
        (
            OSError('No'),
            errors.WriteError('No: {tmp_path}/file/path'),
            'file/path',
        ),
        (
            OSError(errno.EACCES, 'Permission denied'),
            errors.WriteError('Permission denied: {tmp_path}/file/path'),
            'file/path',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_download_catches_exceptions_from_download_to_stream(exception, exp_exception, to, mocker, tmp_path):
    if to:
        to = tmp_path / to
        to.parent.mkdir(parents=True)
        to.write_bytes(b'some bytes')

    mocker.patch(
        'aiobtclientapi.utils._download_to_stream',
        side_effect=exception,
    )

    exp_msg = str(exp_exception).format(tmp_path=tmp_path)
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
        await utils.download('http://localhost:12345', to=to)


@pytest.mark.parametrize(
    argnames='size, maxsize, exp_exception',
    argvalues=(
        (123, None, None),
        (123, 999, None),
        (999, 999, None),
        (1000, 999, errors.ReadError('Too big (1000 bytes): {url}')),
    ),
)
@pytest.mark.asyncio
async def test_download_to_stream(size, maxsize, exp_exception, mocker, tmp_path):
    url = 'http://localhost:12345'
    file = io.BytesIO()

    response_mock = Mock(
        headers={'Content-Length': str(size)},
        aiter_bytes=Mock(return_value=Mock(
            __aiter__=lambda self: self,
            __anext__=AsyncMock(side_effect=[b'pay', b'load', b'data']),
        )),
    )

    stream_mock = Mock(return_value=Mock(
        __aenter__=AsyncMock(return_value=response_mock),
        __aexit__=AsyncMock(return_value=False),
    ))

    AsyncClient_mock = mocker.patch(
        'httpx.AsyncClient',
        return_value=Mock(
            __aenter__=AsyncMock(),
            __aexit__=AsyncMock(return_value=False),
            stream=stream_mock,
        ),
    )

    if exp_exception:
        exp_msg = str(exp_exception).format(url=url)
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
            await utils._download_to_stream(url, file, maxsize)

        assert AsyncClient_mock.call_args_list == [call(
            follow_redirects=True,
            timeout=constants.HTTP_REQUEST_TIMEOUT,
        )]
        assert stream_mock.call_args_list == [call('GET', url)]
        assert response_mock.raise_for_status.call_args_list == [call()]
        assert response_mock.aiter_bytes.call_args_list == []

    else:
        return_value = await utils._download_to_stream(url, file, maxsize)

        assert AsyncClient_mock.call_args_list == [call(
            follow_redirects=True,
            timeout=constants.HTTP_REQUEST_TIMEOUT,
        )]
        assert stream_mock.call_args_list == [call('GET', url)]
        assert response_mock.raise_for_status.call_args_list == [call()]
        assert response_mock.aiter_bytes.call_args_list == [call()]
        assert return_value is None

        assert file.tell() == len(b'payloaddata')
        file.seek(0)
        assert file.read() == b'payloaddata'


@pytest.mark.asyncio
async def test_merge_async_generators():

    async def foo():
        for i in range(6):
            yield f'foo {i}'

    async def bar():
        for i in range(6):
            if i == 3:
                raise errors.Error(f'bar {i}')
            else:
                yield f'bar {i}'

    async def baz():
        for i in range(3):
            yield f'baz {i}'

    merged = []
    async for coro in utils.merge_async_generators(foo(), bar(), baz()):
        try:
            merged.append(await coro)
        except errors.Error as e:
            merged.append(e)

    assert [x for x in merged if str(x).startswith('foo')] == [
        'foo 0',
        'foo 1',
        'foo 2',
        'foo 3',
        'foo 4',
        'foo 5',
    ]
    assert [x for x in merged if str(x).startswith('bar')] == [
        'bar 0',
        'bar 1',
        'bar 2',
        errors.Error('bar 3'),
    ]
    assert [x for x in merged if str(x).startswith('baz')] == [
        'baz 0',
        'baz 1',
        'baz 2',
    ]


@pytest.mark.parametrize(
    argnames='dct, exp_return_value',
    argvalues=(
        (
            {
                'a': 1,
                'b': None,
                'c': '',
                'd': 2,
                'e': None,
                'f': 0,
                'g': None,
                'h': 3,
                'i': False,
            },
            {
                'a': 1,
                'c': '',
                'd': 2,
                'f': 0,
                'h': 3,
                'i': False,
            },
        ),
    ),
)
def test_without_None_values(dct, exp_return_value):
    return_value = utils.without_None_values(dct)
    assert return_value == exp_return_value
