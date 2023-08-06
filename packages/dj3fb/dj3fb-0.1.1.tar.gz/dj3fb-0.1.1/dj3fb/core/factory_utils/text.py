# -*- coding: utf-8 -*-
import re


def camel_case2snake_case(s: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
