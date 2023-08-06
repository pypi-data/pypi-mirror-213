import hmac
from hashlib import sha256
from datetime import datetime
from typing import Optional

from signway_sdk import signing_functions


def sign_url(
        id: str,
        secret: str,
        host: str,
        proxy_url: str,
        expiry: int,
        method: str,
        headers: Optional[dict[str, str]] = None,
        body: Optional[str] = None,
        datetime_override: Optional[datetime] = None
) -> str:
    """Creates a signed URL for SignWay"""
    if not host.endswith('/'):
        host += '/'
    dt = datetime_override or datetime.utcnow()
    headers = headers or {}
    if body is not None:
        headers["Content-Length"] = str(len(body))
    unsigned_url = host + signing_functions.authorization_query_params_no_sig(
        access_key=id,
        dt=dt,
        expires=expiry,
        proxy_url=proxy_url,
        custom_headers=headers or {},
        sign_body=body is not None
    )
    canonical_req = signing_functions.canonical_request(
        method=method,
        url=unsigned_url,
        headers=headers or {},
        body=body or ""
    )
    to_sign = signing_functions.string_to_sign(
        dt=dt,
        canonical_req=canonical_req
    )
    signing_key = signing_functions.signing_key(
        dt=dt,
        secret=secret
    )

    h = hmac.new(signing_key, digestmod=sha256)
    h.update(to_sign.encode())
    signature = h.hexdigest()

    return f'{unsigned_url}&{signing_functions.X_SIGNATURE}={signature}'
