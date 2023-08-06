from unittest.mock import Mock, call

import pytest

import aiobtclientapi


def test_api_classes_returns_expected_classes():
    assert aiobtclientapi.api_classes() == (
        aiobtclientapi.DelugeAPI,
        aiobtclientapi.QbittorrentAPI,
        aiobtclientapi.RtorrentAPI,
        aiobtclientapi.TransmissionAPI,
    )


def test_api_classes_return_value_is_cached():
    return_value = aiobtclientapi.api_classes()
    for _ in range(3):
        assert aiobtclientapi.api_classes() is return_value


def test_client_names(mocker):
    mock_apis = (Mock(), Mock(), Mock())
    mock_apis[0].name = 'foo'
    mock_apis[1].name = 'bar'
    mock_apis[2].name = 'baz'
    mocker.patch('aiobtclientapi.api_classes', return_value=mock_apis)
    assert aiobtclientapi.client_names() == ('foo', 'bar', 'baz')


def test_api_class(mocker):
    mock_apis = (Mock(), Mock(), Mock())
    mock_apis[0].name = 'foo'
    mock_apis[1].name = 'bar'
    mock_apis[2].name = 'baz'
    mocker.patch('aiobtclientapi.api_classes', return_value=mock_apis)

    api = aiobtclientapi.api_class('bar')
    assert api is mock_apis[1]
    assert mock_apis[1].call_args_list == []

    with pytest.raises(aiobtclientapi.ValueError, match=r"^Unknown client: 'asdf'"):
        aiobtclientapi.api_class('asdf')


def test_api(mocker):
    mock_apis = (Mock(), Mock(), Mock())
    mock_apis[0].name = 'foo'
    mock_apis[1].name = 'bar'
    mock_apis[2].name = 'baz'
    mocker.patch('aiobtclientapi.api_classes', return_value=mock_apis)

    api = aiobtclientapi.api('bar', baz=123)
    assert api is mock_apis[1].return_value
    assert mock_apis[1].call_args_list == [call(baz=123)]

    with pytest.raises(aiobtclientapi.ValueError, match=r"^Unknown client: 'asdf'"):
        aiobtclientapi.api('asdf', baz=123)
