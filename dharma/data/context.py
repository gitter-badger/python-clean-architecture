# -*- coding: utf-8 -*-
from collections import defaultdict
from enum import Enum


class AutoValidationStatus(Enum):
    off = 'off'
    # TODO selective autovalidation
    # selective_on
    # selective_off
    on = 'on'


class AutoValidationContext(object):

    def __init__(self, status=None):
        self._status = status or AutoValidationStatus.on
        self._SELECTIVE_ON_REGISTER = defaultdict(lambda: [])
        self._SELECTIVE_OFF_REGISTER = defaultdict(lambda: [])

    def is_to_be_validated(self, nature, trait_name):
        if self._status == ValidationStatus.on:
            return True
        if self._status == ValidationStatus.off:
            return False
        key = (nature.__module__, nature.__class__.__name__, trait_name)
        register = self._SELECTIVE_ON_REGISTER if self._status == ValidationStatus.selective_on else self._SELECTIVE_OFF_REGISTER
        return nature in register[key]


_context = AutoValidationContext()


def get_context():
    return _context
