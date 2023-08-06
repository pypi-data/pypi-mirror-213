from datetime import datetime

from signway_sdk.sign_url import sign_url


def test_sign_url():
    url = sign_url(
        id='foo',
        secret='secret',
        expiry=600,
        method='POST',
        host='http://localhost:3000',
        proxy_url='https://github.com/',
        datetime_override=datetime.utcfromtimestamp(0)
    )

    assert url == f'http://localhost:3000/' \
                  '?X-Sw-Algorithm=SW1-HMAC-SHA256' \
                  '&X-Sw-Credential=foo%2F19700101' \
                  '&X-Sw-Date=19700101T000000Z' \
                  '&X-Sw-Expires=600' \
                  '&X-Sw-Proxy=https%3A%2F%2Fgithub.com%2F' \
                  '&X-Sw-SignedHeaders=' \
                  '&X-Sw-Body=false' \
                  '&X-Sw-Signature=ed15db76d806155fd5119e093a0f030063c90d943dfdd27e011a9044a77a90a6'
