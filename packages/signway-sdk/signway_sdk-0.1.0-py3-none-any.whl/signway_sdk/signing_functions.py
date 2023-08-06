import hmac
from urllib.parse import urlparse, parse_qs, quote, quote_plus
from datetime import datetime
from hashlib import sha256

X_ALGORITHM = "X-Sw-Algorithm"
ALGORITHM = "SW1-HMAC-SHA256"
X_CREDENTIAL = "X-Sw-Credential"
X_DATE = "X-Sw-Date"
X_EXPIRES = "X-Sw-Expires"
X_SIGNED_HEADERS = "X-Sw-SignedHeaders"
X_SIGNED_BODY = "X-Sw-Body"
X_PROXY = "X-Sw-Proxy"
X_SIGNATURE = "X-Sw-Signature"

LONG_DATETIME = '%Y%m%dT%H%M%SZ'
SHORT_DATETIME = '%Y%m%d'


def canonical_uri_string(uri: str) -> str:
    """Actually, just the path"""

    decoded = urlparse(uri)
    return quote(decoded.path)


def canonical_query_string(uri: str) -> str:
    decoded = urlparse(uri)
    qs = parse_qs(decoded.query, keep_blank_values=True)

    params = []
    for param in qs.items():
        k, vs = param
        k_quote = quote_plus(k)
        for v in vs:
            params.append(f"{k_quote}={quote_plus(v)}")
    params.sort()
    return '&'.join(params)


def canonical_header_string(headers: dict[str, str]) -> str:
    headers_list = []
    for k, v in headers.items():
        headers_list.append(f'{k.lower()}:{v.strip()}')
    headers_list.sort()
    return '\n'.join(headers_list)


def signed_header_string(headers: dict[str, str]) -> str:
    headers_list = []
    for k in headers:
        headers_list.append(k.lower())
    headers_list.sort()
    return ';'.join(headers_list)


def canonical_request(method: str, url: str, headers: dict[str, str], body: str) -> str:
    return f"{method}\n" \
           f"{canonical_uri_string(url)}\n" \
           f"{canonical_query_string(url)}\n" \
           f"{canonical_header_string(headers)}\n\n" \
           f"{signed_header_string(headers)}\n" \
           f"{body}"


def scope_string(dt: datetime) -> str:
    return dt.strftime(SHORT_DATETIME)


def string_to_sign(dt: datetime, canonical_req: str) -> str:
    return f"{ALGORITHM}\n" \
           f"{dt.strftime(LONG_DATETIME)}\n" \
           f"{scope_string(dt)}\n" \
           f"{sha256(canonical_req.encode()).hexdigest()}"


def signing_key(dt: datetime, secret: str) -> bytes:
    secret = f'{ALGORITHM}{secret}'
    h = hmac.new(secret.encode(), digestmod=sha256)
    h.update(dt.strftime(SHORT_DATETIME).encode())
    return h.digest()


def authorization_query_params_no_sig(
        access_key: str,
        dt: datetime,
        expires: int,
        proxy_url: str,
        custom_headers: dict[str, str],
        sign_body: bool,
) -> str:
    credentials = f'{access_key}/{scope_string(dt)}'

    signed_headers = []
    for k in custom_headers:
        signed_headers.append(k.lower().strip())

    headers_string = ';'.join(signed_headers)

    parsed_proxy_url = urlparse(proxy_url)

    credentials = quote_plus(credentials)
    headers_string = quote_plus(headers_string)
    proxy_url = quote_plus(parsed_proxy_url.geturl())
    long_date = dt.strftime(LONG_DATETIME)
    sign_body_str = "true" if sign_body else "false"

    return f"?{X_ALGORITHM}={ALGORITHM}" \
           f"&{X_CREDENTIAL}={credentials}" \
           f"&{X_DATE}={long_date}" \
           f"&{X_EXPIRES}={expires}" \
           f"&{X_PROXY}={proxy_url}" \
           f"&{X_SIGNED_HEADERS}={headers_string}" \
           f"&{X_SIGNED_BODY}={sign_body_str}"
