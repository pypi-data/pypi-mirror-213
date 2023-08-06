# -*- coding: utf-8 -*-
import abc
from typing import Tuple, Optional
from django.db import models


class BaseFieldTemplate(abc.ABC):
    f_lib = 'from dj3fb.faker_utils import f'

    def __init__(self, field: models.Field):
        self.field = field

    @abc.abstractmethod
    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        raise NotImplementedError()


class SmallIntegerFieldTemplate(BaseFieldTemplate):
    delta = 0

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        if self.field.choices is not None:
            choices = [k for k, _ in self.field.choices]
            return None, f"factory.Iterator({str(choices)})"
        else:
            return None, f'factory.Sequence(lambda n: n + {self.delta})'


class IntegerFieldTemplate(SmallIntegerFieldTemplate):
    delta = 10000


class BigIntegerFieldTemplate(SmallIntegerFieldTemplate):
    delta = 100000000


class BinaryFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = "memoryview(f.binary(1024))"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class BooleanFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        return self.f_lib, "factory.Sequence(lambda _: f.boolean())"


class CharFieldTemplate(BaseFieldTemplate):
    field: models.CharField

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        if self.field.choices is not None:
            choices = [k for k, _ in self.field.choices]
            return None, f"factory.Iterator({str(choices)})"
        else:
            s = f"f.pystr(max_chars={self.field.max_length or 32})"
            return self.f_lib, f"factory.Sequence(lambda _: {s})"


class DateFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        return self.f_lib, "factory.Sequence(lambda _: f.date_this_century())"


class DateTimeFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        return self.f_lib, "factory.Sequence(lambda _: f.date_time_this_century())"


class DecimalFieldTemplate(BaseFieldTemplate):
    field: models.DecimalField

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        left_digits = None
        if self.field.max_digits is not None and self.field.decimal_places is not None:
            left_digits = self.field.max_digits - self.field.decimal_places

        s = f"f.pydecimal(left_digits={left_digits}, right_digits={self.field.decimal_places})"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class DurationFieldTemplate(BaseFieldTemplate):
    field: models.DurationField

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.time_delta()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class EmailFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.email()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class FilePathFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.file_path()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class FileFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        return None, f"factory.django.FileField()"


class FloatFieldTemplate(BaseFieldTemplate):
    field: models.FloatField

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.pyfloat()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class GenericIPAddressFieldTemplate(BaseFieldTemplate):
    field: models.GenericIPAddressField

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        if self.field.protocol == 'ipv6':
            s = "f.ipv4()"
        else:
            s = "f.ipv6()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class ImageFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        return None, f"factory.django.ImageField()"


class JSONFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.json()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class TextFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.text()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class TimeFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.time()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class URLFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.url()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"


class UUIDFieldTemplate(BaseFieldTemplate):

    def get_fake_expression(self) -> Tuple[Optional[str], str]:
        s = f"f.uuid4()"
        return self.f_lib, f"factory.Sequence(lambda _: {s})"
