"""Run under Xvfb with a D-Bus session; GI callbacks must not hide errors."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
Gtk.init()
import main
from category import Category
from snippet import Snippet
from files import load_data, save_data


class WindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = main.Application()
        cls.app.register(None)

    def setUp(self):
        self.callback_errors = []
        self.old_hook = sys.excepthook
        sys.excepthook = lambda *error: self.callback_errors.append(error)
        self.addCleanup(setattr, sys, 'excepthook', self.old_hook)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'chosen.col'
        self.window = main.MainWindow(application=self.app)
        self.addCleanup(self.window.close)
        save_data(['Different title', [Category('Category', 1), [
            Snippet('Category', 'First', 1, content='first', tags=['one']),
            Snippet('Category', 'Second', 1, content='second', tags=['two']),
            Snippet('Category', 'Third', 1, tags=['three'])]]], self.path)

    def tearDown(self):
        self.assertEqual(self.callback_errors, [], 'Unhandled GTK callback exception')

    def select_first(self):
        self.window.open_collection(self.path)
        categories = self.window.listbox
        row = categories.get_row_at_index(0)
        self.window.listbox_category_row_clicked(categories, row)
        snippets = self.window.listbox
        self.window.listbox_snippet_row_clicked(snippets, snippets.get_row_at_index(0), 0)
        return categories, row

    def test_window_start_and_open(self):
        self.window.present()
        self.assertEqual(self.window.stack.get_visible_child_name(), 'welcome')
        self.window.open_collection(self.path)
        self.assertEqual(self.window.stack.get_visible_child_name(), 'content')
        self.assertEqual(self.window.collection_path, self.path.resolve())
        self.assertFalse(self.window.button_edit.get_sensitive())
        self.assertEqual(self.window.tag_list_refresh(), ['one', 'two', 'three'])

    def test_edit_save_and_switch_snippet(self):
        self.select_first()
        toggle = self.window.button_edit
        toggle.set_active(True)
        self.assertTrue(self.window.content_sourceview.get_editable())
        self.window.content_sourceview.get_buffer().set_text('edited')
        snippets = self.window.listbox
        self.window.listbox_snippet_row_clicked(snippets, snippets.get_row_at_index(1), 0)
        loaded = load_data(self.path)
        self.assertEqual(loaded[1][1][0].content, 'edited')
        self.assertEqual(loaded[1][1][1].content, 'second')
        self.assertIs(self.window.button_edit, toggle)
        self.assertFalse(toggle.get_active())
        self.assertFalse(self.window.content_sourceview.get_editable())

    def test_add_and_delete_category(self):
        self.window.open_collection(self.path)
        entry = Gtk.Entry(text='New')
        self.window.listbox_add_category(None, entry)
        self.assertEqual(len(load_data(self.path)), 3)
        self.window.button_delete_category(None, self.window.listbox, None, 1)
        self.assertEqual(len(load_data(self.path)), 2)
        entry.set_text('  ')
        self.window.listbox_add_category(None, entry)
        self.assertEqual(len(load_data(self.path)), 2)

    def test_add_delete_snippet_and_reset_editor(self):
        categories, row = self.select_first()
        self.window.button_add_snippet(None, Gtk.Entry(text='Fourth'), categories, row)
        self.assertEqual(len(load_data(self.path)[1][1]), 4)
        self.window.button_delete_snippet(None, categories, row, 0)
        self.assertEqual(len(load_data(self.path)[1][1]), 3)
        self.assertIsNone(self.window.active_snippet)
        self.assertFalse(self.window.button_edit.get_sensitive())

    def test_failed_open_preserves_current_collection(self):
        self.window.open_collection(self.path)
        current = self.window.data
        broken = self.path.parent / 'broken.col'
        broken.write_text('bad')
        with self.assertRaises(main.CollectionError):
            self.window.open_collection(broken)
        self.assertIs(self.window.data, current)
        self.assertEqual(self.window.collection_path, self.path.resolve())

    def test_new_collection_through_save_dialog(self):
        path = self.path.parent / 'new.col'
        class File:
            def get_path(self):
                return str(path)
        class Dialog:
            def __init__(self, **kwargs):
                self.callbacks = {}
            def connect(self, signal, callback):
                self.callbacks[signal] = callback
            def present(self):
                self.callbacks['response'](self, Gtk.ResponseType.OK)
            def get_file(self):
                return File()
            def __getattr__(self, name):
                return lambda *args: None
        with patch.object(Gtk, 'FileChooserDialog', Dialog):
            self.window.button_new_file(None, Gtk.Entry(text='../New'))
        self.assertEqual(load_data(path), ['../New'])
        self.assertEqual(self.window.collection_path, path.resolve())

    def test_failed_save_keeps_editor_and_selected_snippet(self):
        self.select_first()
        original = self.window.active_snippet
        self.window.button_edit.set_active(True)
        self.window.content_sourceview.get_buffer().set_text('unsaved')
        with patch('main.save_data', side_effect=OSError('disk full')), \
                patch.object(self.window, 'show_error') as error:
            snippets = self.window.listbox
            self.window.listbox_snippet_row_clicked(snippets, snippets.get_row_at_index(1), 0)
            self.assertIs(self.window.active_snippet, original)
            self.assertTrue(self.window.button_edit.get_active())
            self.assertTrue(self.window.content_sourceview.get_editable())
            self.assertTrue(self.window.on_close_request(self.window))
            error.assert_called()
        self.window.button_edit.set_active(False)
        self.assertEqual(load_data(self.path)[1][1][0].content, 'unsaved')

    def test_close_saves_active_edit(self):
        self.select_first()
        self.window.button_edit.set_active(True)
        self.window.content_sourceview.get_buffer().set_text('save on close')
        self.assertFalse(self.window.on_close_request(self.window))
        self.assertEqual(load_data(self.path)[1][1][0].content, 'save on close')
