import functools
import inspect
import re

import pytest

from aiobtclientapi import errors

error_classes = tuple(
    value
    for name, value in inspect.getmembers(errors)
    if inspect.isclass(value) and issubclass(value, BaseException)
)


@functools.lru_cache()
def get_hierarchy_from_docstring():
    print(errors.__doc__)

    map = {}
    regex = re.compile(r'^    (.*?)([a-zA-Z]+)')
    parents = [Exception]
    indent_step_size = 0
    prev_cls = None
    level = prev_level = 0

    for line in errors.__doc__.split('\n'):
        match = regex.search(line)
        if match:
            indent = len(match.group(1))
            cls = getattr(errors, match.group(2))

            # Character width of one indentation level
            if indent and indent_step_size <= 0:
                indent_step_size = indent

            # How deep are we indented?
            if indent_step_size > 0:
                level = int(indent / indent_step_size)

            level_diff = level - prev_level
            if level_diff > 0:
                level_diff += level_diff
                parents.append(prev_cls)

            elif level_diff < 0:
                while level_diff < 0 and parents:
                    parents.pop(-1)
                    level_diff += 1

            map[cls] = tuple(parents)

            prev_level = level
            prev_cls = cls

    return map

@pytest.mark.parametrize('cls', error_classes)
def test_parents_as_documented(cls):
    hierarchy = get_hierarchy_from_docstring()

    try:
        parents = hierarchy[cls]
    except KeyError:
        raise RuntimeError(f'Undocumented exception: {cls.__name__}')

    for parent in parents:
        assert issubclass(cls, parent)


def test_builtin_parents():
    assert issubclass(errors.ValueError, ValueError)
    assert issubclass(errors.NotImplementedError, NotImplementedError)
    assert issubclass(errors.ConnectionError, ConnectionError)
    assert issubclass(errors.TimeoutError, TimeoutError)


@pytest.mark.parametrize('error_cls', error_classes)
@pytest.mark.parametrize(
    argnames='arg1, arg2, exp_equal',
    argvalues=(
        ('foo', 'foo', True),
        ('foo', 'bar', False),
    ),
    ids=lambda v: repr(v),
)
def test_equality(error_cls, arg1, arg2, exp_equal):
    if error_cls in (errors.TorrentWarning,):
        pytest.skip(f'{error_cls.__name__} is supposed to be used as a subclass only')
    else:
        e1 = error_cls(arg1)
        e2 = error_cls(arg2)
        assert (e1 == e2) is exp_equal
        assert (e1 != e2) is not exp_equal


@pytest.mark.parametrize(
    argnames='arg, exp_cause',
    argvalues=(
        ('Something went wrong', None),
        (errors.Error('Something went wrong'), errors.Error('Something went wrong')),
    ),
    ids=lambda v: repr(v),
)
def test_ResponseError(arg, exp_cause):
    class FooResponseError(errors.ResponseError):
        def __init__(self, arg, bar, *, baz):
            self.bar = bar
            self.baz = baz

    e = FooResponseError(arg, 'Bar', baz='Baz')
    assert e.cause == exp_cause
    assert e.bar == 'Bar'
    assert e.baz == 'Baz'


@pytest.mark.parametrize(
    argnames='error_cls, exp_msg',
    argvalues=(
        (errors.NoSuchTorrentError, 'No such torrent: {arg}'),
        (errors.InvalidTorrentError, 'Invalid torrent: {arg}'),
        (errors.AddTorrentError, 'Adding torrent failed: {arg}'),
        (errors.StartTorrentError, 'Starting torrent failed: {arg}'),
        (errors.StopTorrentError, 'Stopping torrent failed: {arg}'),
        (errors.VerifyTorrentError, 'Verifying torrent failed: {arg}'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='arg, exp_cause',
    argvalues=(
        ('Something went wrong', None),
        (errors.Error('Something went wrong'), errors.Error('Something went wrong')),
    ),
    ids=lambda v: repr(v),
)
def test_ResponseError_subclass(error_cls, arg, exp_msg, exp_cause):
    exp_msg = exp_msg.format(arg=arg)
    e = error_cls(arg)
    assert str(e) == exp_msg
    assert e.cause == exp_cause


@pytest.mark.parametrize(
    argnames='infohash, name, msg_with_name, msg_without_name, exp_exception, exp_msg, exp_infohash, exp_name',
    argvalues=(
        (
            'd34db33f', None,
            'Foo: {name}: {infohash}',
            'Foo: {infohash}',
            None, 'Foo: d34db33f', 'd34db33f', None,
        ),
        (
            'd34db33f', 'MyTorrent',
            'Foo: {name}: {infohash}',
            'Foo: {infohash}',
            None, 'Foo: MyTorrent: d34db33f', 'd34db33f', 'MyTorrent',
        ),
        (
            'd34db33f', 'MyTorrent',
            NotImplemented,
            'Foo: {infohash}',
            RuntimeError('You are supposed to subclass {cls_name}'),
            None, None, None,
        ),
    ),
)
def test_TorrentWarning(infohash, name, msg_with_name, msg_without_name, exp_exception, exp_msg, exp_infohash, exp_name):
    class FooTorrentWarning(errors.TorrentWarning):
        _msg_with_name = msg_with_name
        _msg_without_name = msg_without_name

    if exp_exception:
        exp_msg = str(exp_exception).format(cls_name='FooTorrentWarning')
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
            FooTorrentWarning(infohash, name=name)
    else:
        e = FooTorrentWarning(infohash, name=name)
        assert str(e) == exp_msg
        assert e.infohash == exp_infohash
        assert e.name == exp_name


@pytest.mark.parametrize('error_cls', [
    cls for cls in error_classes
    if (
        issubclass(cls, errors.TorrentWarning)
        and cls is not errors.TorrentWarning
    )
])
@pytest.mark.parametrize(
    argnames='infohash, name, exp_msg_format',
    argvalues=(
        ('d34db33f', None, '_msg_without_name'),
        ('d34db33f', 'MyTorrent', '_msg_with_name'),
    ),
)
def test_TorrentWarning_subclass(error_cls, infohash, name, exp_msg_format):
    exp_msg = getattr(error_cls, exp_msg_format).format(infohash=infohash, name=name)
    e = error_cls(infohash, name=name)
    assert str(e) == exp_msg
