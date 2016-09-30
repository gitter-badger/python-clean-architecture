# -*- coding: utf-8 -*-
import re

from dharma.exceptions import TraitValidationError
from dharma.utils import OrderedSet


def construct_validators(genus):
    return ()


def min_len(length):
    def min_len_validator(value):
        if len(value) < length:
            raise TraitValidationError(
                message="Value {0} doesn't fulfill min length of {1}".format(value, length))
    min_len_validator.length = length
    return min_len_validator


def max_len(length):
    def max_len_validator(value):
        if len(value) > length:
            raise TraitValidationError("Value doesn't ")
    max_len_validator.length = length
    return max_len_validator


def check_elements(iterable):
    def elements_validator(value):
        if any(e not in iterable for e in iterable):
            raise TraitValidationError
    elements_validator.elements = iterable
    return elements_validator


def regex(pattern, message, flags=None):
    re_object = re.compile(pattern, flags=flags)

    def regex_validator(value):
        if not re_object.match(value):
            raise TraitValidationError()
    regex_validator.pattern = pattern
    return regex_validator

