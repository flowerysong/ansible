# Copyright (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class EventSource:
    def __init__(self):
        self._handlers = set()

    def __iadd__(self, handler):
        if not callable(handler):
            raise ValueError('handler must be callable')
        self._handlers.add(handler)
        return self

    def __isub__(self, handler):
        try:
            self._handlers.remove(handler)
        except KeyError:
            pass

        return self

    def _on_exception(self, handler, exc, *args, **kwargs):
        pass

    def fire(self, *args, **kwargs):
        for h in self._handlers:
            try:
                h(*args, **kwargs)
            except Exception as ex:
                self._on_exception(h, ex, *args, **kwargs)
