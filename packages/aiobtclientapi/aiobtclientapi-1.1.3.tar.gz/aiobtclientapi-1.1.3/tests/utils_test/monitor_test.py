import re
from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from aiobtclientapi import errors
from aiobtclientapi.utils import monitor


@pytest.mark.parametrize('negate', (False, True), ids=lambda v: repr(v))
@pytest.mark.parametrize('return_value', ('foo', 'bar'), ids=lambda v: repr(v))
@pytest.mark.asyncio
async def test_Monitor_return_value_equals(return_value, negate, mocker):
    block_until_mock = mocker.patch('aiobtclientapi.utils.monitor.Monitor._block_until')

    value = 'bar'
    await monitor.Monitor(AsyncMock()).return_value_equals(value, negate=negate)
    condition = block_until_mock.call_args_list[0].args[0]

    result = condition(return_value)
    exp_result = bool(return_value != value) if negate else bool(return_value == value)
    assert result is exp_result


@pytest.mark.parametrize('negate', (False, True), ids=lambda v: repr(v))
@pytest.mark.parametrize('return_value', (Ellipsis, NotImplemented), ids=lambda v: repr(v))
@pytest.mark.asyncio
async def test_Monitor_return_value_is(return_value, negate, mocker):
    block_until_mock = mocker.patch('aiobtclientapi.utils.monitor.Monitor._block_until')

    value = Ellipsis
    await monitor.Monitor(AsyncMock()).return_value_is(value, negate=negate)
    condition = block_until_mock.call_args_list[0].args[0]

    result = condition(return_value)
    exp_result = bool(return_value is not value) if negate else bool(return_value is value)
    assert result is exp_result


@pytest.mark.parametrize('negate', (False, True), ids=lambda v: repr(v))
@pytest.mark.parametrize('return_value', (['foo', 'baz'], ['foo', 'bar']), ids=lambda v: repr(v))
@pytest.mark.asyncio
async def test_Monitor_return_value_contains(return_value, negate, mocker):
    block_until_mock = mocker.patch('aiobtclientapi.utils.monitor.Monitor._block_until')

    value = 'bar'
    await monitor.Monitor(AsyncMock()).return_value_contains(value, negate=negate)
    condition = block_until_mock.call_args_list[0].args[0]

    result = condition(return_value)
    exp_result = bool(value not in return_value) if negate else bool(value in return_value)
    assert result is exp_result


@pytest.mark.parametrize('negate', (False, True), ids=lambda v: repr(v))
@pytest.mark.parametrize('return_value', ('foo', 'bar'), ids=lambda v: repr(v))
@pytest.mark.asyncio
async def test_Monitor_return_value_validates(return_value, negate, mocker):
    block_until_mock = mocker.patch('aiobtclientapi.utils.monitor.Monitor._block_until')

    def validator(return_value):
        return return_value == 'bar'

    await monitor.Monitor(AsyncMock()).return_value_validates(validator, negate=negate)
    condition = block_until_mock.call_args_list[0].args[0]

    result = condition(return_value)
    exp_result = bool(return_value != 'bar') if negate else bool(return_value == 'bar')
    assert result is exp_result


@pytest.mark.asyncio
async def test_Monitor_block_until():
    call_return_values = ['foo1', 'foo2', 'bar', 'baz']

    async def call():
        return call_return_values.pop(0)

    def condition(return_value):
        return return_value == 'bar'

    m = monitor.Monitor(
        call=call,
        timeout=0.1,
        interval=0.01,
    )

    return_value = await m._block_until(condition)
    assert return_value == 'bar'
    assert call_return_values == ['baz']


@pytest.mark.asyncio
async def test_Monitor_block_until_attribute():
    call_return_values = [
        Mock(this='foo1', that='foo'),
        Mock(this='foo2', that='bar'),
        Mock(this='bar'),
        Mock(this='baz'),
    ]

    async def call():
        return call_return_values.pop(0)

    def condition(return_value):
        return return_value == 'bar'

    m = monitor.Monitor(
        call=call,
        attribute='this',
        timeout=0.1,
        interval=0.01,
    )

    return_value = await m._block_until(condition)
    assert return_value == 'bar'
    assert len(call_return_values) == 1
    assert call_return_values[0].this == 'baz'


@pytest.mark.asyncio
async def test_Monitor_block_until_timeout():
    call = AsyncMock(return_value='foo')
    m = monitor.Monitor(
        call=call,
        timeout=0.1,
        interval=0.01,
    )

    def condition(return_value):
        return False

    with pytest.raises(errors.TimeoutError, match=r'Timeout after 0.1 seconds'):
        await m._block_until(condition)

    for c in call.call_args_list:
        assert c == call.call_args_list[0]
    # call() should be called 10 times, maybe a little less
    assert 9 <= len(call.call_args_list) <= 10


@pytest.mark.parametrize(
    argnames='interval, exp_sleep, exp_exception',
    argvalues=(
        (123, 123, None),
        (1.23, 1.23, None),
        (Mock(__class__=monitor.DynamicInterval, next=AsyncMock(return_value=12.3)), 12.3, None),
        ('a billion years', None, RuntimeError("Invalid interval: 'a billion years'")),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_Monitor_sleep(interval, exp_sleep, exp_exception, mocker):
    sleep_mock = mocker.patch('asyncio.sleep')

    m = monitor.Monitor(
        call=AsyncMock(),
        interval=interval,
    )

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await m._sleep()
    else:
        await m._sleep()
        assert sleep_mock.call_args_list == [call(exp_sleep)]


@pytest.mark.asyncio
async def test_DynamicInterval_progress():
    di = monitor.DynamicInterval(min=min, max=max, progress_getter=AsyncMock(), name='test')
    mock_progress = Mock()
    di._progress = mock_progress
    assert di.progress is mock_progress


@pytest.mark.parametrize(
    argnames='seconds, exp_sleep_calls',
    argvalues=(
        (-1, []),
        (0, []),
        (0.01, [call(0.01)]),
        (123, [call(123)]),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_DynamicInterval_sleep(seconds, exp_sleep_calls, mocker):
    sleep_mock = mocker.patch('asyncio.sleep')
    mocker.patch('aiobtclientapi.utils.monitor.DynamicInterval.next', return_value=seconds)

    di = monitor.DynamicInterval(min=min, max=max, progress_getter=AsyncMock(), name='test')
    await di.sleep()
    assert sleep_mock.call_args_list == exp_sleep_calls


@pytest.mark.parametrize(
    argnames='min, max, seconds_left, exp_interval',
    argvalues=(
        (1, 12, -1, 1),
        (2, 12, -1, 2),
        (3, 12, -1, 3),
        (3, 12, 60, 12),
        (3, 12, 48, 12),
        (3, 12, 36, 12),
        (3, 12, 30, 10),
        (3, 12, 27, 9),
        (3, 12, 24, 8),
        (3, 12, 18, 6),
        (3, 12, 12, 4),
        (3, 12, 9, 3),
        (3, 12, 7, 3),
        (3, 12, 6, 3),
        (3, 12, 5, 3),
        (3, 12, 3, 3),
        (3, 12, 2, 3),
        (3, 12, 0, 3),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_DynamicInterval_next(min, max, seconds_left, exp_interval, mocker):
    maintain_samples_mock = mocker.patch(
        'aiobtclientapi.utils.monitor.DynamicInterval._maintain_samples',
    )
    get_seconds_left_mock = mocker.patch(
        'aiobtclientapi.utils.monitor.DynamicInterval._get_seconds_left',
        return_value=seconds_left,
    )

    di = monitor.DynamicInterval(min=min, max=max, progress_getter=AsyncMock(), name='test')

    return_value = await di.next()
    assert return_value == exp_interval
    assert maintain_samples_mock.call_args_list == [call()]
    assert get_seconds_left_mock.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='samples, exp_seconds_left',
    argvalues=(
        ([(1000, 3), (1001, 3)], -1),
        ([(1000, 30), (2000, 30), (3000, 30)], -1),
        ([(1000, 30), (2000, 29), (3000, 28)], -1),

        ([(1000, 30), (-1, -1), (1003, 42)], 14.5),
        ([(1000, 30), (-1, -1), (1006, 42)], 29),

        ([(1000, 90), (-1, -1), (1012, 96)], 8),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_DynamicInterval_get_seconds_left(samples, exp_seconds_left, mocker):
    di = monitor.DynamicInterval(min=1, max=3, progress_getter=AsyncMock(), name='test')
    di._samples = samples

    return_value = await di._get_seconds_left()
    assert return_value == exp_seconds_left


@pytest.mark.parametrize(
    argnames='samples, progress, exp_samples, exp_exception',
    argvalues=(
        ([], -1, [], AssertionError('-1')),
        ([], 101, [], AssertionError('101')),
        ([], 42.123, [(1000, 42.123)], None),
        ([(1, 10), (2, 20), (3, 30), (4, 40)], 42.123, [(3, 30), (4, 40), (1000, 42.123)], None),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_DynamicInterval_maintain_samples(samples, progress, exp_samples, exp_exception, mocker):
    progress_getter = AsyncMock(return_value=progress)
    print('->', progress_getter.return_value)

    di = monitor.DynamicInterval(min=1, max=3, progress_getter=progress_getter, name='test')
    di._samples = list(samples)

    with patch('time.monotonic', side_effect=range(1000, 2000)):
        if exp_exception:
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
                await di._maintain_samples()
        else:
            await di._maintain_samples()

    assert di._samples == exp_samples
    assert di._progress_getter.call_args_list == [call()]
