from __future__ import annotations

import json
import logging
import re

from ulid import ULID

from leanit_mweb.orm.exception import ValidationFailedException

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Field:
    def __init__(self, default=None):
        self.default = default

    def to_db(self, value):
        """
        convert python value to db value
        :param value:
        :return:
        """
        return value

    def from_db(self, value):
        """
        convert value from db value to python value
        :param value:
        :return:
        """
        return value

    def get_default(self):
        if callable(self.default):
            return self.default()
        else:
            return self.default

    def validate(self, value):
        """
        might raise ValidationFailedException
        :param value:
        :return:
        """
        pass


class IntegerField(Field):
    pass


class StringField(Field):
    def __init__(self, min_length=None, max_length=None, default=None, alphabet=None):
        super().__init__(default=default)
        self.min_length = min_length
        self.max_length = max_length
        self.alphabet = alphabet

    def validate(self, value):
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationFailedException(f"String is too short: '{value}'")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationFailedException(f"String is too long: '{value}'")
        if self.alphabet is not None and not set(value).issubset(set(self.alphabet)):
            raise ValidationFailedException(f"String contains invalid characters: '{value}'")
        return super().validate(value)


class EmailField(StringField):
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

    def validate(self, value):
        # validate email
        if not self.pattern.match(value):
            raise ValidationFailedException(f"Invalid email: '{value}'")



class UlidField(StringField):
    def get_default(self):
        return str(ULID())


class DateTimeField(Field):
    pass

class BooleanField(Field):
    # psycopg2 does support boolean type correctly, no need to convert string to boolean and vice versa
    pass

class JsonField(StringField):
    # psycopg2 handles reads correctly and automatically converts json to python dict
    # but it does not handle writes correctly, so we need to convert python dict to json string
    def to_db(self, value):
        return json.dumps(value)
