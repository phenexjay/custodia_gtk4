import json
import os
from pathlib import Path
import pickle
import tempfile
import unittest
from unittest.mock import patch

from category import Category
from snippet import Snippet
from files import CollectionError, load_data, save_data

ROOT = Path(__file__).resolve().parents[1]


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'selected.col'
        self.data = ['../Name außerhalb', [Category('Python', 1), [
            Snippet('Python', 'Grüße', 2, content='print("Hallo")', tags=['GTK'])]]]

    def test_json_roundtrip_uses_selected_path(self):
        save_data(self.data, self.path)
        self.assertEqual(json.loads(self.path.read_text())['version'], 1)
        loaded = load_data(self.path)
        self.assertEqual(loaded[0], self.data[0])
        self.assertEqual(loaded[1][1][0].content, 'print("Hallo")')
        self.assertEqual(loaded[1][1][0].tags, ['GTK'])
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_bundled_legacy_import_and_json_conversion(self):
        loaded = load_data(ROOT / 'saves/default.col')
        self.assertEqual(len(loaded) - 1, 3)
        self.assertEqual(sum(len(items) for _, items in loaded[1:]), 7)
        save_data(loaded, self.path)
        self.assertEqual(load_data(self.path)[1][0].title, loaded[1][0].title)
        self.assertTrue(self.path.read_text().startswith('{'))

    def test_arbitrary_pickle_globals_are_rejected(self):
        marker = self.path.parent / 'executed'
        class Payload:
            def __reduce__(self):
                return os.system, (f'touch {marker}',)
        self.path.write_bytes(pickle.dumps(Payload()))
        with self.assertRaises(CollectionError):
            load_data(self.path)
        self.assertFalse(marker.exists())

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_data(self.path)

    def test_invalid_files(self):
        for content in [b'', b'garbage', b'[]', b'{}', b'\x80\x05',
                        b'{"version":2,"title":"x","categories":[]}',
                        b'{"version":1,"title":3,"categories":[]}']:
            with self.subTest(content=content):
                self.path.write_bytes(content)
                with self.assertRaises(CollectionError):
                    load_data(self.path)

    def test_failed_replace_preserves_original_and_cleans_temporary(self):
        self.path.write_text('original')
        with patch('files.os.replace', side_effect=OSError('disk error')):
            with self.assertRaises(OSError):
                save_data(self.data, self.path)
        self.assertEqual(self.path.read_text(), 'original')
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_data_does_not_replace_original(self):
        self.path.write_text('original')
        self.data[1][1][0].tags = 'not a list'
        with self.assertRaises(CollectionError):
            save_data(self.data, self.path)
        self.assertEqual(self.path.read_text(), 'original')

    def test_tags_are_owned_by_each_snippet(self):
        a, b = Snippet('c', 'a', 1), Snippet('c', 'b', 1)
        a.tags.append('one')
        self.assertEqual(b.tags, [])
        tags = ['two']
        c = Snippet('c', 'c', 1, tags=tags)
        tags.append('three')
        self.assertEqual(c.tags, ['two'])
