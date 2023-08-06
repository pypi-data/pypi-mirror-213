import errno
import os
import re
from unittest.mock import Mock, call, patch

import pytest

from aiobtclientapi import errors
from aiobtclientapi.clients.rtorrent import utils as rtorrent_utils


@pytest.mark.parametrize(
    argnames='bad_filename, exception, exp_exception',
    argvalues=(
        (None, None, None),
        ('bar', FileNotFoundError('no such file'), None),
        ('bar', PermissionError('permission denied'), errors.ReadError('permission denied: {filepath}')),
        ('bar', OSError(errno.EACCES, 'permission denied'), errors.ReadError('permission denied: {filepath}')),
    ),
    ids=lambda v: repr(v),
)
def test_parent_classes(bad_filename, exception, exp_exception, mocker):
    location = 'path/to/location'
    files2piece_indexes = {
        'foo': [1, 3, 6],
        'bar': [12],
        'baz': [36, 60, 72, 96],
    }
    mtimes = {
        'foo': 123,
        'bar': 456,
        'baz': 789,
    }

    filestream_mock = Mock(
        get_piece_indexes_of_file=Mock(side_effect=lambda file: files2piece_indexes[file]),
    )
    TorrentFileStream_mock = mocker.patch('torf.TorrentFileStream', return_value=Mock(
        __enter__=Mock(return_value=filestream_mock),
        # Return False to raise any exception from the managed context
        __exit__=Mock(return_value=False),
    ))

    def mtime_mock(path):
        filename = os.path.basename(path)
        if filename == bad_filename:
            raise exception
        else:
            return Mock(st_mtime=mtimes[filename])

    torrent = Mock(
        files=list(files2piece_indexes),
        pieces=sum(len(piece_indexes) for piece_indexes in files2piece_indexes.values()),
        metainfo={'mock': 'metainfo'},
        dump=Mock(),
    )

    exp_libtorrent_resume = {
        'files': [
            {'completed': 3, 'priority': 0, 'mtime': mtimes['foo']},
            {'completed': 1, 'priority': 0, 'mtime': mtimes['bar']},
            {'completed': 4, 'priority': 0, 'mtime': mtimes['baz']},
        ],
        'bitfield': torrent.pieces,
    }
    if bad_filename:
        bad_filename_index = torrent.files.index(bad_filename)
        del exp_libtorrent_resume['files'][bad_filename_index]['mtime']

    if exp_exception:
        exp_msg = str(exp_exception).format(filepath=os.path.join(location, bad_filename))
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
            with patch('os.stat', Mock(side_effect=mtime_mock)):
                rtorrent_utils.add_resume_fields(torrent, location)
        assert torrent.metainfo == {
            'mock': 'metainfo',
        }

    else:
        with patch('os.stat', Mock(side_effect=mtime_mock)):
            rtorrent_utils.add_resume_fields(torrent, location)

        assert torrent.metainfo == {
            'mock': 'metainfo',
            'libtorrent_resume': exp_libtorrent_resume,
        }

    assert TorrentFileStream_mock.call_args_list == [call(torrent, content_path=location)]

    exp_get_piece_indexes_of_file_calls = [call(file) for file in files2piece_indexes]
    if bad_filename and exp_exception:
        del exp_get_piece_indexes_of_file_calls[torrent.files.index(bad_filename) + 1:]
    assert filestream_mock.get_piece_indexes_of_file.call_args_list == exp_get_piece_indexes_of_file_calls
