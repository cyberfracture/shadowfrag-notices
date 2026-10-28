"""Validate the public, text-only SHADOWFRAG notices feed before publishing."""
import datetime
import json
from pathlib import Path
import re


def text(value, limit, multiline=False):
    assert isinstance(value, str), 'Expected text'
    assert 0 < len(value.encode('utf-8')) <= limit, 'Text exceeds its byte limit'
    assert value.strip(), 'Text must not be blank'
    assert all(ord(c) >= 32 or (multiline and c == '\n') for c in value), 'Control character'
    assert all(not 127 <= ord(c) <= 159 for c in value), 'Control character'
    assert not any(c in value for c in ('\u202a', '\u202b', '\u202c', '\u202d', '\u202e',
                                        '\u2066', '\u2067', '\u2068', '\u2069')), 'Bidi control'


def notice(item):
    assert isinstance(item, dict), 'Notice must be an object'
    assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}', item['id']), 'Invalid ID'
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['date']), 'Invalid date format'
    datetime.date.fromisoformat(item['date'])
    text(item['title'], 96)
    text(item['summary'], 240)
    text(item['body'], 4000, multiline=True)
    assert isinstance(item['sample'], bool), 'sample must be a boolean'


def main():
    raw = Path(__file__).with_name('notices.json').read_bytes()
    assert len(raw) <= 65536, 'Feed exceeds 64 KiB'
    feed = json.loads(raw)
    assert type(feed['schema_version']) is int and feed['schema_version'] == 1, 'Unsupported schema'
    items = feed['notices']
    assert isinstance(items, list) and len(items) <= 20, 'Too many notices'
    for item in items:
        notice(item)
    assert len({item['id'] for item in items}) == len(items), 'Duplicate ID'
    print(f'Valid: {len(items)} notices, {len(raw)} bytes')


if __name__ == '__main__':
    main()
