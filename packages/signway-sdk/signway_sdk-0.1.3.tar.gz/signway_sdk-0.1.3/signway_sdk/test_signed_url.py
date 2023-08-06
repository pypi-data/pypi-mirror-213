import os
import time

import requests

from signway_sdk.sign_url import sign_url

ID = os.environ.get("SW_ID", "my-id")
SECRET = os.environ.get("SW_SECRET", "my-secret")
HOST = os.environ.get("SW_HOST", 'http://localhost:3000')


def test_empty():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='GET',
        proxy_url='https://postman-echo.com/get',
    )

    res = requests.get(url).json()

    assert res['url'] == 'https://postman-echo.com/get'


def test_with_params():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='GET',
        proxy_url='https://postman-echo.com/get?param=1',
    )

    res = requests.get(url).json()

    assert res['args']['param'] == '1'


def test_with_headers():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='GET',
        headers={'X-Foo': 'foo'},
        proxy_url='https://postman-echo.com/get?param=1',
    )

    res = requests.get(url, headers={'X-Foo': 'foo'})
    res = res.json()

    assert res['headers']['x-foo'] == 'foo'


def test_with_body():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='POST',
        headers={'X-Foo': 'foo'},
        body='{"foo": "bar"}',
        proxy_url='https://postman-echo.com/post?param=1',
    )

    res = requests.post(url, headers={'X-Foo': 'foo'}, data='{"foo": "bar"}')
    res = res.json()

    assert res['json']['foo'] == 'bar'


def test_expired():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=1,
        method='GET',
        proxy_url='https://postman-echo.com/get',
    )

    time.sleep(1)

    res = requests.get(url)
    assert res.status_code == 400


def test_non_present_header():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='GET',
        headers={'X-Foo': 'foo'},
        proxy_url='https://postman-echo.com/get',
    )

    res = requests.get(url)
    assert res.status_code == 400


def test_bad_header_value():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='GET',
        headers={'X-Foo': 'foo'},
        proxy_url='https://postman-echo.com/get',
    )

    res = requests.get(url, headers={"X-Foo": 'bar'})
    assert res.status_code == 400


def test_bad_body():
    url = sign_url(
        id=ID,
        secret=SECRET,
        host=HOST,
        expiry=10,
        method='POST',
        body='{"foo": "bar"}',
        proxy_url='https://postman-echo.com/post',
    )

    res = requests.post(url, data='{"foo": "baz"}')
    assert res.status_code == 400
