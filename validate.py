"""Validate the public, text-only SHADOWFRAG notices feed before publishing."""
import datetime
import ipaddress
import json
from pathlib import Path
import re
import ssl


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


def host(value):
    text(value, 253)
    try:
        ipaddress.ip_address(value)
        return
    except ValueError:
        pass
    assert not re.fullmatch(r'[0-9.]+', value), 'Invalid numeric address'
    for label in value.split('.'):
        assert re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', label), 'Invalid hostname'


def certificate(value):
    assert isinstance(value, str) and len(value.encode('utf-8')) <= 4096, 'Invalid certificate size'
    assert re.fullmatch(r'-----BEGIN CERTIFICATE-----\n[A-Za-z0-9+/=\n]+-----END CERTIFICATE-----[\r\n ]*', value), 'Only a public certificate is allowed'
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cadata=value)
    assert context.cert_store_stats()['x509_ca'] == 1, 'A public CA certificate is required'


def server(item):
    assert isinstance(item, dict), 'Server must be an object'
    assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}', item['id']), 'Invalid server ID'
    text(item['name'], 80)
    text(item['description'], 240)
    host(item['address'])
    host(item['server_name'])
    for name in ('port', 'protocol'):
        assert type(item[name]) is int and 1 <= item[name] <= 65535, f'Invalid {name}'
    certificate(item['trust_pem'])


def server_list(items):
    assert isinstance(items, list) and len(items) <= 32, 'Too many servers'
    for item in items:
        server(item)
    assert len({item['id'] for item in items}) == len(items), 'Duplicate server ID'
    assert len({(item['address'].lower(), item['port']) for item in items}) == len(items), 'Duplicate server address'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, 'Duplicate JSON key'
        result[key] = value
    return result


def main():
    raw = Path(__file__).with_name('notices.json').read_bytes()
    assert len(raw) <= 65536, 'Feed exceeds 64 KiB'
    feed = json.loads(raw, object_pairs_hook=unique_object)
    assert type(feed['schema_version']) is int and feed['schema_version'] == 1, 'Unsupported schema'
    items = feed['notices']
    assert isinstance(items, list) and len(items) <= 20, 'Too many notices'
    for item in items:
        notice(item)
    assert len({item['id'] for item in items}) == len(items), 'Duplicate ID'
    servers = feed.get('servers', [])
    server_list(servers)
    print(f'Valid: {len(items)} notices, {len(servers)} servers, {len(raw)} bytes')


if __name__ == '__main__':
    main()
