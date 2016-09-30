# -*- coding: utf-8 -*-
import six

from dharma.utils.collections import OrderedSet

from .trait import Trait
from . import validation


def string(min_len=None, max_len=None, chars=None, validators=None):
    validator_set = OrderedSet()
    if min_len is not None:
        validator_set.add(validation.min_len(min_len))
    if max_len is not None:
        validator_set.add(validation.max_len(max_len))
    if chars is not None:
        validator_set.add(validation.check_elements(chars))
    if validators:
        validator_set |= validators
    return Trait(six.text_type, validators=validators)


IPv4_RE = r'^(?:(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)\.){3}(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)$'


def ip():
    validator = validation.regex(IPv4_RE, "")
    return Trait(six.text_type, validators=[validator])
