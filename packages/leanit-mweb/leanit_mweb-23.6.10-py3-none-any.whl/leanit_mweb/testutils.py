from __future__ import annotations
import logging
import re

from httpx import Response
from starlette.testclient import TestClient

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

class Form:

    def __init__(self, action, method, data):
        self.action = action
        # always lowercase
        self.method = method
        self.data = data

    def fill(self, **kwargs):
        self.data.update(kwargs)

    @classmethod
    def from_response(cls, response: Response, index=None, name=None, id=None):
        return cls.parse(response.text, index=index, name=name, id=id)

    @classmethod
    def parse(cls, html, index=None, name=None, id=None):
        all_forms = re.findall(r'<form.+?</form>', html, flags=re.DOTALL)

        if index is not None:
            form_html = all_forms[index]
        elif name is not None:
            form_html = [form for form in all_forms if f'name="{name}"' in form][0]
        elif id is not None:
            form_html = [form for form in all_forms if f'id="{id}"' in form][0]
        elif len(all_forms) == 1:
            form_html = all_forms[0]
        elif len(all_forms) == 0:
            raise ValueError("No form found")
        else:
            raise ValueError("Multiple forms found, specify index, name or id")

        action = re.search(r'action\s*=\s*["\'](.+?)["\']', form_html).group(1)
        method = re.search(r'method\s*=\s*["\'](.+?)["\']', form_html).group(1).lower()
        inputs = re.findall(r'<input.+?>', form_html, flags=re.DOTALL)

        data = {}
        for input in inputs:
            name_match = re.search(r'name\s*=\s*["\'](.+?)["\']', input)
            if not name_match:
                continue
            name = name_match.group(1)

            type_match = re.search(r'type\s*=\s*["\'](.+?)["\']', input)
            type = type_match.group(1) if type_match else 'text'

            if type == 'checkbox':
                checked_match = re.search(r'checked', input)
                value = bool(checked_match)
            else:
                value_match = re.search(r'value\s*=\s*["\'](.+?)["\']', input)
                value = value_match.group(1) if value_match else ''

            data[name] = value

        return cls(action, method, data)

    def submit(self, client: TestClient, **kwargs) -> Response:
        if "follow_redirects" not in kwargs:
            kwargs["allow_redirects"] = False

        if self.method == 'post':
            return client.post(self.action, data=self.data, **kwargs)
        elif self.method == 'get':
            return client.get(self.action, params=self.data, **kwargs)
        else:
            raise ValueError(f"Unknown method: {self.method}")
