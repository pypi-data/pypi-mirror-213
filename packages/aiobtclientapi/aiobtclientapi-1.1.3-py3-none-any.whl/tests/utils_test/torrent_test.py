import errno
import io
import os
import re
from unittest.mock import Mock, call

import pytest
import torf

from aiobtclientapi import constants, errors, utils


def get_asset(filename):
    return os.path.join(
        os.path.dirname(__file__),
        '../assets',
        filename,
    )

torrent_file_good = get_asset('good.torrent')
torrent_file_badly_encoded = get_asset('badly_encoded.torrent')
torrent_file_bad_metainfo = get_asset('bad_metainfo.torrent')
torrent_file_looks_like_magnet = get_asset('magnet:?xt=urn:btih:7ca88dbff0402541801dc36ce0d4a0403ae7f99a&dn=this_is_a_file')

with open(torrent_file_good, 'rb') as f:
    torrent_bytes_good = f.read()
with open(torrent_file_badly_encoded, 'rb') as f:
    torrent_bytes_badly_encoded = f.read()
with open(torrent_file_bad_metainfo, 'rb') as f:
    torrent_bytes_bad_metainfo = f.read()

magnet_uri_good = 'magnet:?xt=urn:btih:7ca88dbff0402541801dc36ce0d4a0403ae7f99a&dn=foo.jpg&xl=1328'
magnet_uri_bad = 'magnet:?xt=urn:btih:7ca88dbff0402541801dc36ce0d4a0403ae7f99a&dn=foo.jpg&xl=hello'


@pytest.mark.parametrize(
    argnames='torrent, exp_result',
    argvalues=(
        # Raw byte strings
        (torrent_bytes_good, torf.Torrent.read_stream(io.BytesIO(torrent_bytes_good))),
        (torrent_bytes_badly_encoded, errors.InvalidTorrentError('Invalid metainfo format')),
        (
            torrent_bytes_bad_metainfo,
            errors.InvalidTorrentError("Invalid metainfo: Missing 'piece length' in ['info']"),
        ),
        (
            Mock(read=Mock(side_effect=OSError('No errno provided'))),
            errors.ReadError('Failed to read'),
        ),

        # File-like object
        (io.BytesIO(torrent_bytes_good), torf.Torrent.read_stream(io.BytesIO(torrent_bytes_good))),
        (io.BytesIO(torrent_bytes_badly_encoded), errors.InvalidTorrentError('Invalid metainfo format')),
        (
            io.BytesIO(torrent_bytes_bad_metainfo),
            errors.InvalidTorrentError("Invalid metainfo: Missing 'piece length' in ['info']"),
        ),

        # Torrent file path
        (torrent_file_good, torf.Torrent.read(torrent_file_good)),
        (torrent_file_looks_like_magnet, torf.Torrent.read(torrent_file_looks_like_magnet)),
        (torrent_file_badly_encoded, errors.InvalidTorrentError(torrent_file_badly_encoded)),
        (
            torrent_file_bad_metainfo,
            errors.InvalidTorrentError("Invalid metainfo: Missing 'piece length' in ['info']: {file}"),
        ),
        ('/no/such/file.torrent', errors.ReadError(f'{os.strerror(errno.ENOENT)}: /no/such/file.torrent')),

        # Magnet URI
        (magnet_uri_good, torf.Magnet.from_string(magnet_uri_good).torrent()),
        (magnet_uri_bad, errors.InvalidTorrentError(f'Invalid exact length ("xl"): {magnet_uri_bad}')),

    ),
)
def test_read(torrent, exp_result):
    if isinstance(exp_result, BaseException):
        exp_msg = str(exp_result).format(file=torrent)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(exp_msg)}$'):
            utils.torrent.read(torrent)
    else:
        return_value = utils.torrent.read(torrent)
        assert return_value == exp_result


def test_read_bytes(mocker):
    read_bytes_upstream = mocker.patch('aiobtclientapi.utils.read_bytes')
    return_value = utils.torrent.read_bytes('foo')
    assert return_value is read_bytes_upstream.return_value
    assert read_bytes_upstream.call_args_list == [call('foo', maxsize=constants.MAX_TORRENT_SIZE)]


@pytest.mark.asyncio
async def test_download_bytes(mocker):
    download_upstream = mocker.patch('aiobtclientapi.utils.download')
    return_value = await utils.torrent.download_bytes('foo')
    assert return_value is download_upstream.return_value
    assert download_upstream.call_args_list == [call('foo', maxsize=constants.MAX_TORRENT_SIZE)]


@pytest.mark.parametrize(
    argnames='torrent, exp_infohash',
    argvalues=(
        (
            'F000000000000000000000000000000000000000',
            'f000000000000000000000000000000000000000',
        ),
        (
            torrent_file_good,
            '7ca88dbff0402541801dc36ce0d4a0403ae7f99a',
        ),
        (
            open(torrent_file_good, 'rb').read(),
            '7ca88dbff0402541801dc36ce0d4a0403ae7f99a',
        ),
    ),
)
def test_get_infohash(torrent, exp_infohash, mocker):
    infohash = utils.torrent.get_infohash(torrent)
    assert infohash == exp_infohash
    assert isinstance(infohash, utils.Infohash)
