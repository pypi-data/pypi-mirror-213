import asyncio
import re
import types
from unittest.mock import AsyncMock, Mock, call

import pytest

from aiobtclientapi import errors, response


def test_Response_mro():
    import types
    assert response.Response.mro() == [
        response.Response,
        types.SimpleNamespace,
        object,
    ]


@pytest.mark.parametrize(
    argnames='arguments, exp_attributes, exp_exception',
    argvalues=(
        ({}, {}, TypeError("__init__() missing 1 required keyword-only argument: 'success'")),
        (
            {'success': 0, 'errors': ('a', 'b', 'c'), 'warnings': range(3), 'tasks': ('this', 'that'), 'foo': 'bar'},
            {'success': False, 'errors': ['a', 'b', 'c'], 'warnings': [0, 1, 2], 'tasks': ['this', 'that'], 'foo': 'bar'},
            None,
        ),
    ),
)
def test_Response_attributes(arguments, exp_attributes, exp_exception):
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'{re.escape(str(exp_exception))}$'):
            response.Response(**arguments)
    else:
        r = response.Response(**arguments)
        for name, value in exp_attributes.items():
            assert getattr(r, name) == value
        assert r.as_dict == exp_attributes


@pytest.mark.parametrize(
    argnames='attributes',
    argvalues=(
        None,
        {},
        {'foo': 123, 'bar': ['b', 'a', 'z']},
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_Response_from_call_assembles_initial_attributes(attributes, mocker):
    HandleResults_mock = mocker.patch('aiobtclientapi.response._HandleResults')

    exp_initial_attributes = {
        'success': True,
        'warnings': [],
        'errors': [],
        'tasks': [],
    }
    if attributes is not None:
        exp_initial_attributes.update(attributes)
    HandleResults_mock.return_value.attributes = exp_initial_attributes

    exp_types = {
        'success': bool,
        'warnings': errors.Warning,
        'errors': errors.Error,
    }

    r = await response.Response.from_call(
        call=AsyncMock()(),
        attributes=attributes,
        exception='mock wrapped exception',
    )
    assert r.as_dict == exp_initial_attributes
    assert HandleResults_mock.call_args_list == [
        call(exp_initial_attributes, exp_types, 'mock wrapped exception'),
    ]


@pytest.mark.parametrize(
    argnames='attributes, types, exp_exception',
    argvalues=(
        ({}, {}, None),
        ({'foo': 'bar'}, {'foo': str}, None),
        ({'foo': 'bar'}, {'baz': str}, AssertionError()),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_Response_from_call_assembles_all_types(attributes, types, exp_exception, mocker):
    HandleResults_mock = mocker.patch('aiobtclientapi.response._HandleResults')
    HandleResults_mock.return_value.attributes = {'success': True}

    exp_initial_attributes = {
        **attributes,
        **{
            'success': True,
            'warnings': [],
            'errors': [],
            'tasks': [],
        },
    }

    exp_types = {
        'success': bool,
        'warnings': errors.Warning,
        'errors': errors.Error,
    }
    if types is not None:
        exp_types.update(types)

    task = asyncio.create_task(AsyncMock()())
    try:
        coro = response.Response.from_call(
            call=task,
            attributes=attributes,
            types=types,
            exception='MockExceptionWrapper',
        )
        if exp_exception:
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
                await coro
        else:
            await coro
            assert HandleResults_mock.call_args_list == [
                call(exp_initial_attributes, exp_types, 'MockExceptionWrapper'),
            ]
    finally:
        task.cancel()


@pytest.mark.parametrize(
    argnames='call, exp_handler_calls, exp_exception',
    argvalues=(
        # Coroutine without error
        (AsyncMock(return_value='foo')(), [call('foo')], None),

        # Coroutine with error
        (AsyncMock(side_effect=errors.Error('foo'))(), [call(errors.Error('foo'))], None),

        # Asynchronous generator without error
        (
            Mock(
                __class__=types.AsyncGeneratorType,
                __aiter__=lambda self: self,
                __anext__=AsyncMock(side_effect=['foo', 'bar', 'baz']),
            ),
            [call('foo'), call('bar'), call('baz')],
            None,
        ),

        # Asynchronous generator with error
        (
            Mock(
                __class__=types.AsyncGeneratorType,
                __aiter__=lambda self: self,
                __anext__=AsyncMock(side_effect=['foo', errors.Error('arg'), 'baz']),
            ),
            [call('foo'), call(errors.Error('arg'))],
            None,
        ),

        # Unsupported call type
        (
            'not a proper call',
            [],
            RuntimeError("Unsupported type: str: 'not a proper call'")
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_Response_from_call_calls_handler(call, exp_handler_calls, exp_exception, mocker):
    HandleResults_mock = mocker.patch('aiobtclientapi.response._HandleResults')
    handler = HandleResults_mock.return_value
    handler.attributes = {'success': True}

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await response.Response.from_call(call)
        assert handler.call_args_list == []
    else:
        await response.Response.from_call(call)
        assert handler.call_args_list == exp_handler_calls


def test_HandleResults_properties():
    initial_attributes = {'a': 'b'}
    types = {'a': str}
    exception = errors.ResponseError
    h = response._HandleResults(initial_attributes, types, exception)
    assert h.attributes is initial_attributes
    assert h._types is types
    assert h.exception is exception


@pytest.mark.parametrize(
    argnames='result, exp_result',
    argvalues=(
        ((), RuntimeError("Invalid result: ()")),
        (('foo',), RuntimeError("Invalid result: ('foo',)")),
        ((1, 'foo'), RuntimeError("Invalid result: (1, 'foo')")),
        (('foo', 'bar', 'baz'), RuntimeError("Invalid result: ('foo', 'bar', 'baz')")),
        (('foo', 'bar'), [call('foo', 'bar')]),
        (('bar', 'foo'), [call('bar', 'foo')]),
    ),
    ids=lambda v: repr(v),
)
def test_HandleResults_call_gets_tuple(result, exp_result, mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_pair')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    if isinstance(exp_result, BaseException):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            h(result)
    else:
        h(result)
        assert h.handle_pair.call_args_list == exp_result


def test_HandleResults_call_gets_Error(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_errors')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    h(errors.Error('foo'))
    assert h.handle_errors.call_args_list == [call(errors.Error('foo'))]
    h(errors.ReadError('bar'))
    assert h.handle_errors.call_args_list == [
        call(errors.Error('foo')),
        call(errors.ReadError('bar')),
    ]


def test_HandleResults_call_gets_Warning(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_warnings')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    h(errors.Warning('foo'))
    assert h.handle_warnings.call_args_list == [call(errors.Warning('foo'))]
    h(errors.TorrentAlreadyStarted('bar'))
    assert h.handle_warnings.call_args_list == [
        call(errors.Warning('foo')),
        call(errors.TorrentAlreadyStarted('bar')),
    ]


def test_HandleResults_call_gets_Response(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_responses')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    r = response.Response(success=True, warnings=['foo'], errors=['bar'])
    h(r)
    assert h.handle_responses.call_args_list == [call(r)]


@pytest.mark.asyncio
async def test_HandleResults_call_gets_Task(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_tasks')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    task = asyncio.Task(AsyncMock()())
    h(task)
    assert h.handle_tasks.call_args_list == [call(task)]


def test_HandleResults_call_gets_NotImplementedError():
    h = response._HandleResults(initial_attributes={'errors': []}, types={}, exception=None)
    h(NotImplementedError('foo'))
    assert h.attributes == {'errors': [errors.NotImplementedError(NotImplementedError('foo'))]}


@pytest.mark.parametrize('exception', (BaseException('foo'), KeyboardInterrupt('bar')))
def test_HandleResults_call_gets_BaseException(exception):
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
        h(exception)


def test_HandleResults_call_gets_None(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults.handle_pair')
    mocker.patch('aiobtclientapi.response._HandleResults.handle_errors')
    mocker.patch('aiobtclientapi.response._HandleResults.handle_warnings')
    mocker.patch('aiobtclientapi.response._HandleResults.handle_responses')
    mocker.patch('aiobtclientapi.response._HandleResults.handle_tasks')
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    h(None)
    assert h.handle_pair.call_args_list == []
    assert h.handle_errors.call_args_list == []
    assert h.handle_warnings.call_args_list == []
    assert h.handle_responses.call_args_list == []
    assert h.handle_tasks.call_args_list == []


@pytest.mark.parametrize('something', ('foo', 123, ['bar']))
def test_HandleResults_call_gets_something_else(something):
    h = response._HandleResults(initial_attributes=None, types={}, exception=None)
    with pytest.raises(RuntimeError, match=rf'^Invalid result: {re.escape(repr(something))}$'):
        h(something)


@pytest.mark.parametrize('attribute', ('success', 'errors', 'warnings', 'tasks'))
def test_HandleResults_handle_pair_forwards_generic_attribute(attribute, mocker):
    mocker.patch(f'aiobtclientapi.response._HandleResults.handle_{attribute}')
    h = response._HandleResults(
        initial_attributes={'success': True,
                            'errors': [],
                            'warnings': [],
                            'tasks': []},
        types={},
        exception=None,
    )
    h.handle_pair(attribute, 'foo')
    assert getattr(h, f'handle_{attribute}').call_args_list == [call('foo')]


def test_HandleResults_handle_pair_appends_to_list_attribute(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults._ensure_type', return_value='type ensured')
    h = response._HandleResults(
        initial_attributes={'foo': [], 'bar': 'baz'},
        types={},
        exception=None,
    )
    h.handle_pair('foo', 123)
    assert h.attributes['foo'] == ['type ensured']
    assert h._ensure_type.call_args_list == [call('foo', 123)]


def test_HandleResults_handle_pair_overwrites_nonlist_attribute(mocker):
    mocker.patch('aiobtclientapi.response._HandleResults._ensure_type', return_value='type ensured')
    h = response._HandleResults(
        initial_attributes={'foo': [], 'bar': 'baz'},
        types={},
        exception=None,
    )
    h.handle_pair('bar', 123)
    assert h.attributes['bar'] == 'type ensured'
    assert h._ensure_type.call_args_list == [call('bar', 123)]


def test_HandleResults_handle_pair_gets_unknown_attribute():
    h = response._HandleResults(
        initial_attributes={'foo': [], 'bar': 'baz'},
        types={},
        exception=None,
    )
    with pytest.raises(RuntimeError, match=r"^Unknown attribute: 'BAZ'$"):
        h.handle_pair('BAZ', 123)
    assert h.attributes == {'foo': [], 'bar': 'baz'}


@pytest.mark.parametrize(
    argnames='old_value, new_value, exp_ensure_type_calls, exp_value',
    argvalues=(
        (False, True, [], False),
        (False, False, [], False),
        (True, True, [call('success', True)], True),
        (True, False, [call('success', False)], False),
    ),
)
def test_HandleResults_handle_success(old_value, new_value, exp_ensure_type_calls, exp_value, mocker):
    mocker.patch('aiobtclientapi.response._HandleResults._ensure_type', Mock(
        side_effect=lambda name, value: f'converted:{name}={value}',
    ))
    h = response._HandleResults(
        initial_attributes={'success': 'initial value', 'bar': 'baz'},
        types={},
        exception=None,
    )
    h.attributes['success'] = old_value

    h.handle_success(new_value)
    if exp_ensure_type_calls:
        assert h.attributes['success'] == f'converted:success={exp_value}'
    else:
        assert h.attributes['success'] == old_value
    assert h._ensure_type.call_args_list == exp_ensure_type_calls


def test_HandleResults_handle_errors():
    class Wrapper:
        def __init__(self, exc):
            self.wrapped = exc

        def __eq__(self, other):
            return type(self) == type(other) and str(self.wrapped) == str(other.wrapped)

        def __repr__(self):
            return f'Wrapper({self.wrapped!r})'

    h = response._HandleResults(
        initial_attributes={'errors': [], 'success': True, 'bar': 'baz'},
        types={},
        exception=Wrapper,
    )

    h.handle_errors(errors.Error('foo'))
    assert h.attributes['success'] is False
    assert h.attributes['errors'] == [Wrapper(errors.Error('foo'))]

    h._exc = None
    h.handle_errors(errors.Error('bar'))
    assert h.attributes['success'] is False
    assert h.attributes['errors'] == [Wrapper(errors.Error('foo')), errors.Error('bar')]


def test_HandleResults_handle_warnings():
    h = response._HandleResults(
        initial_attributes={'warnings': [], 'bar': 'baz'},
        types={},
        exception=None,
    )
    h.handle_warnings(errors.Warning('foo'))
    assert h.attributes['warnings'] == [errors.Warning('foo')]
    h.handle_warnings(errors.TorrentAlreadyAdded('bar'))
    assert h.attributes['warnings'] == [errors.Warning('foo'), errors.TorrentAlreadyAdded('bar')]


@pytest.mark.parametrize(
    argnames='initial_success, success, exp_success',
    argvalues=(
        (True, True, True),
        (True, False, False),
        (False, False, False),
        (False, True, False),
    ),
)
def test_HandleResults_handle_responses(initial_success, success, exp_success):
    h = response._HandleResults(
        initial_attributes={
            'success': initial_success,
            'errors': ['a'],
            'warnings': ['b'],
            'bar': 'baz',
        },
        types={},
        exception=None,
    )
    r = response.Response(success=success, errors=['foo'], warnings=['bar'])
    h.handle_responses(r)
    assert h.attributes['errors'] == ['a', 'foo']
    assert h.attributes['warnings'] == ['b', 'bar']
    assert h.attributes['success'] == exp_success


@pytest.mark.asyncio
async def test_HandleResults_handle_tasks():
    h = response._HandleResults(
        initial_attributes={'tasks': [], 'bar': 'baz'},
        types={},
        exception=None,
    )
    task = asyncio.Task(AsyncMock()())
    h.handle_tasks(task)
    assert h.attributes['tasks'] == [task]


def test_HandleResults_ensure_type():
    h = response._HandleResults(
        initial_attributes={'foo': '123', 'bar': 'baz'},
        types={'foo': int},
        exception=None,
    )

    return_value = h._ensure_type('foo', '456')
    assert return_value == 456
    return_value = h._ensure_type('bar', '789')
    assert return_value == '789'
    return_value = h._ensure_type('bar', ['789'])
    assert return_value == ['789']
