from typing import Dict

import yarl

from ...const import APP_BASE_HOST, APP_SECURE_SCHEME
from ...core import HttpCore
from ...exception import TiebaServerError
from ...helper import parse_json
from ...request import pack_form_request, send_request


def parse_body(body: bytes) -> Dict[str, str]:
    res_json = parse_json(body)
    if code := int(res_json['error_code']):
        raise TiebaServerError(code, res_json['error_msg'])

    cates = res_json['cates']

    return cates


async def request(http_core: HttpCore, fname: str) -> Dict[str, str]:
    data = [
        ('BDUSS', http_core.account._BDUSS),
        ('word', fname),
    ]

    request = pack_form_request(
        http_core,
        yarl.URL.build(scheme=APP_SECURE_SCHEME, host=APP_BASE_HOST, path="/c/c/bawu/goodlist"),
        data,
    )

    __log__ = "fname={fname}"  # noqa: F841

    body = await send_request(request, http_core.network, read_bufsize=1024)
    return parse_body(body)
