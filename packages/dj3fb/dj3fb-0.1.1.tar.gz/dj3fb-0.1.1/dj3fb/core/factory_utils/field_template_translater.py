# -*- coding: utf-8 -*-
from typing import Dict, Type
from django.db import models

from .field_templates import BaseFieldTemplate,  IntegerFieldTemplate, BinaryFieldTemplate, BooleanFieldTemplate, \
    CharFieldTemplate, DateFieldTemplate, DateTimeFieldTemplate, DecimalFieldTemplate, DurationFieldTemplate, \
    EmailFieldTemplate, FileFieldTemplate, FilePathFieldTemplate, FloatFieldTemplate, GenericIPAddressFieldTemplate, \
    ImageFieldTemplate, JSONFieldTemplate, TextFieldTemplate, TimeFieldTemplate, \
    URLFieldTemplate, UUIDFieldTemplate, BigIntegerFieldTemplate, SmallIntegerFieldTemplate


class FieldTemplateTranslater:
    cached_mappings = dict()
    mappings: Dict[Type[models.Field], Type[BaseFieldTemplate]] = {
        models.BigIntegerField: BigIntegerFieldTemplate,
        models.BinaryField: BinaryFieldTemplate,
        models.BooleanField: BooleanFieldTemplate,
        models.CharField: CharFieldTemplate,
        models.DateField: DateFieldTemplate,
        models.DateTimeField: DateTimeFieldTemplate,
        models.DecimalField: DecimalFieldTemplate,
        models.DurationField: DurationFieldTemplate,
        models.EmailField: EmailFieldTemplate,
        models.FileField: FileFieldTemplate,
        models.FilePathField: FilePathFieldTemplate,
        models.FloatField: FloatFieldTemplate,
        models.GenericIPAddressField: GenericIPAddressFieldTemplate,
        models.ImageField: ImageFieldTemplate,
        models.IntegerField: IntegerFieldTemplate,
        models.JSONField: JSONFieldTemplate,
        models.PositiveIntegerField: IntegerFieldTemplate,
        models.PositiveBigIntegerField: BigIntegerFieldTemplate,
        models.PositiveSmallIntegerField: SmallIntegerFieldTemplate,
        models.SlugField: CharFieldTemplate,
        models.SmallIntegerField: IntegerFieldTemplate,
        models.TextField: TextFieldTemplate,
        models.TimeField: TimeFieldTemplate,
        models.URLField: URLFieldTemplate,
        models.UUIDField: UUIDFieldTemplate,
    }

    @classmethod
    def translate(cls, field_instance: models.Field) -> BaseFieldTemplate:
        field_template_cls = cls._get_field_template_cls(type(field_instance))
        return field_template_cls(field_instance)

    @classmethod
    def _get_field_template_cls(cls, field_cls) -> Type[BaseFieldTemplate]:
        cls_name = field_cls.__name__

        cache_result = cls.cached_mappings.get(cls_name, None)
        if cache_result is not None:
            return cache_result

        for f_cls in field_cls.__mro__:
            json_field_cls = cls.mappings.get(f_cls, None)
            if json_field_cls is not None:
                cls.cached_mappings[cls_name] = json_field_cls
                return json_field_cls

        raise TypeError(f"{cls_name} can not find corresponding field class.")
