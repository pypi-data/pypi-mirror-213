#!/usr/bin/env python3

"""
comboboxtext:an enriched Gtk.ComboBoxText class
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import bisect

# Assume gtk availability check done at application level
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def block_unblock(method):
    "wrapper function / decorator to block and unblock signal a handler"

    def inner(self, *args, **kwargs): 
        "first block signal handler, call func, then unblock"
        if self._block_count == 0:
            for handler_id, _ in self._handlers:
                self.handler_block(handler_id)
        self._block_count += 1
        rval = method(self, *args, **kwargs)
        if self._block_count == 1:
            for handler_id, _ in self._handlers:
                self.handler_unblock(handler_id)
        self._block_count -= 1
        return rval

    return inner


class ComboBoxText(Gtk.ComboBoxText):
    """Enriched combox, which allows for better manipulation of entries.
       The basic idea is that the list of entries is maintained within 
       the class. Some functions are overwritten to maintain this list
       of entries. Additional functions include: 
       - text_already_present
       - insert_text_sorted
       - text_remove_text
       - update_entries
       - entries

       Note that a signal handler is blocked when manipulating the 
       combobox programmatically. It will only fire on a user selecting a
       different entry.
    """

    def __init__(self):
        super().__init__()
        self._entries = []
        self._handlers = []
        self._block_count = 0

    def connect(self, signal, handler):
        handler_id = Gtk.ComboBoxText.connect(self, signal, handler)
        self._handlers.append((handler_id, handler))
        return handler_id

    def disconnect(self, handler_id):
        self.__super__().disconnect(self, handler_id)
        for listed_id, listed_func in self._handlers:
            if listed_id == handler_id:
                self._handler_ids.remove((listed_id, listed_func))

    def disconnect_by_func(self, func):
        self.__super__().disconnect_by_func(self, func)
        for listed_id, listed_func in self._handlers:
            if listed_func == fun:
                self._handler_ids.remove((listed_id, listed_func))

    @block_unblock
    def insert_text(self, pos, text_id, text):
        super().insert(pos, text_id, text)
        npos = len(self._entries) if pos < 0 else pos
        self._entries.insert(npos, text)

    @block_unblock
    def append_text(self, text):
        super().append_text(text)
        self._entries.append(text)

    def text_already_present(self, text):
        "Returns a Bool indicating of the text is already in the entries"
        return text in self._entries

    @block_unblock
    def insert_text_sorted(self, text, duplicates=False):
        "Inserts text sorted into the combobox"
        if not duplicates and self.text_already_present(text):
            return
        pos = bisect.bisect_left(self._entries, text)
        self.insert_text(pos, None, text)

    @block_unblock
    def text_remove(pos):
        super().text_remove(self, pos)
        self._entries.pop(pos)

    #@block_unblock
    def remove_all(self):
        #super().remove_all()
        super().remove_all()
        self._entries = []

    @block_unblock
    def text_remove_text(self, text):
        "Removes the text if if is already in the list of entries"
        pos = 0
        for entry in self._entries:
            if entry == text:
                self.test_remove(pos)
                return
            pos += 1

    @block_unblock
    def update_entries(self, entries):
        "Updates the complete list of entries with a new list"
        active_entry = self.get_active_text()
        self.remove_all()
        for entry in entries:
            self.append_text(entry)
        pos = 0
        for entry in self._entries:
            if entry == active_entry:
                self.set_active(pos)
                return
            pos += 1
        if len(self._entries) > 0:
            self.set_active(0)

    @block_unblock
    def set_active_text(self, text):
        "Set the given text as active if it exists"
        pos = 0
        for entry in self._entries:
            if entry == text:
                self.set_active(pos)
                return True
            pos += 1
        self.set_active(0)
        return False

    def entries(self):
        "Returns a list of entries"
        return self._entries


