from __future__ import annotations
import logging

from starlette.requests import Request


logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def camelCaseToSnakeCase(name):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in name]).lstrip('_')

def merge_dict(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        elif isinstance(value, list):
            # get node or create one
            node = destination.setdefault(key, [])
            for item in value:
                if item not in node:
                    node.append(item)
        else:
            destination[key] = value

    return destination

def remote_ip(request: Request):
    """
    Return the remote ip address of the request depending on the ip_mode config.
    """
    from leanit_mweb import config
    ip_mode = config.get("mweb", {}).get("ip_mode", "remote_addr")

    if ip_mode == "remote_addr":
        return request.client.host
    elif ip_mode == "x_forwarded_for":
        return request.headers.get("x-forwarded-for", request.client.host)
    elif ip_mode == "cloudflare":
        return request.headers.get("cf-connecting-ip", request.client.host)
    else:
        raise NotImplementedError(f"Unknown ip_mode: {ip_mode}")
