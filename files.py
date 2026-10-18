"""Versioned JSON collections, with restricted import of legacy .col files."""
import io
import json
import math
import os
from pathlib import Path
import pickle
import tempfile

import category
import snippet


class CollectionError(ValueError):
    """A collection has an unsupported or invalid structure."""


class _LegacyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {('category', 'Category'): category.Category,
                   ('snippet', 'Snippet'): snippet.Snippet}
        try:
            return allowed[module, name]
        except KeyError:
            raise CollectionError('Nicht erlaubter Inhalt in alter Kollektion.') from None


def _text(value):
    if not isinstance(value, str):
        raise CollectionError('Textfeld erwartet.')
    return value


def _timestamp(value, optional=False):
    if optional and value == '':
        return value
    if type(value) not in (int, float) or not math.isfinite(value):
        raise CollectionError('Ungültiger Zeitstempel.')
    # The UI formats timestamps using datetime.fromtimestamp.
    from datetime import datetime
    try:
        datetime.fromtimestamp(value)
    except (ValueError, OverflowError, OSError) as exc:
        raise CollectionError('Ungültiger Zeitstempel.') from exc
    return value


def _decode(document):
    try:
        if type(document['version']) is not int or document['version'] != 1:
            raise CollectionError('Unbekannte Dateiversion.')
        data = [_text(document['title'])]
        if not isinstance(document['categories'], list):
            raise CollectionError('Kategorienliste erwartet.')
        for group in document['categories']:
            cat = category.Category(_text(group['title']), _timestamp(group['created']))
            if not isinstance(group['snippets'], list):
                raise CollectionError('Snippetliste erwartet.')
            items = []
            for item in group['snippets']:
                tags = item['tags']
                if tags is None:  # legacy collections may contain None
                    tags = []
                if not isinstance(tags, list):
                    raise CollectionError('Tagliste erwartet.')
                items.append(snippet.Snippet(
                    _text(item['category']), _text(item['title']),
                    _timestamp(item['created']), _timestamp(item['changed'], optional=True),
                    _text(item['content']), _text(item['language']),
                    _text(item['description']), [_text(tag) for tag in tags]))
            data.append([cat, items])
        return data
    except (KeyError, TypeError, IndexError, AttributeError, OverflowError, OSError) as exc:
        raise CollectionError('Ungültige Kollektionsstruktur.') from exc


def _encode(data):
    try:
        return {'version': 1, 'title': data[0], 'categories': [
            {'title': cat.title, 'created': cat.created, 'snippets': [
                {key: getattr(item, key) for key in (
                    'category', 'title', 'created', 'changed', 'content',
                    'language', 'description', 'tags')}
                for item in items]}
            for cat, items in data[1:]]}
    except (TypeError, IndexError, AttributeError, ValueError) as exc:
        raise CollectionError('Ungültige Kollektionsstruktur.') from exc


def save_data(data, path):
    """Atomically replace the explicitly selected file, never a title-derived path."""
    document = _encode(data)
    _decode(document)
    destination = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=destination.parent, delete=False) as stream:
            temporary = stream.name
            json.dump(document, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)


def load_data(path):
    """Read JSON or import legacy objects without permitting arbitrary globals."""
    raw = Path(path).read_bytes()
    if not raw:
        raise CollectionError('Die Kollektion ist leer.')
    try:
        if raw.startswith(b'\x80'):
            document = _encode(_LegacyUnpickler(io.BytesIO(raw)).load())
        else:
            document = json.loads(raw.decode('utf-8'))
        return _decode(document)
    except CollectionError:
        raise
    except (ValueError, UnicodeError, pickle.UnpicklingError, EOFError,
            TypeError, AttributeError, OverflowError) as exc:
        raise CollectionError('Die Kollektion konnte nicht gelesen werden.') from exc
