"""Public directory contract checks; run python3 -m unittest before publishing."""
import copy
import json
from pathlib import Path
import unittest
import validate


class DirectoryValidation(unittest.TestCase):
    def setUp(self):
        self.item = json.loads(Path(__file__).with_name('notices.json').read_text())['servers'][0]

    def test_current_public_identity(self):
        validate.server(self.item)
        validate.server_list([])

    def test_reject_hostile_entries(self):
        fields = [
            ('id', '../secret'), ('name', 'bad\u202econtrol'),
            ('address', 'https://example.com'), ('address', 'bad host'),
            ('address', '999.999.999.999'), ('server_name', '*.example.com'),
            ('port', True), ('port', 0), ('port', 65536), ('protocol', 44.0),
            ('trust_pem', 'not a certificate'),
            ('trust_pem', self.item['trust_pem'] + '-----BEGIN PRIVATE KEY-----\n'),
        ]
        for name, value in fields:
            with self.subTest(field=name, value=value):
                item = copy.deepcopy(self.item)
                item[name] = value
                with self.assertRaises((AssertionError, ValueError)):
                    validate.server(item)

    def test_duplicate_identity_and_bounds(self):
        with self.assertRaises(AssertionError):
            validate.server_list([self.item, self.item])
        other = dict(self.item, id='another')
        with self.assertRaises(AssertionError):
            validate.server_list([self.item, other])
        with self.assertRaises(AssertionError):
            validate.server_list([self.item] * 33)

    def test_hostname_and_ipv6(self):
        for address in ('play.example.com', '192.0.2.4', '2001:db8::1'):
            validate.host(address)

    def test_duplicate_json_key(self):
        with self.assertRaises(AssertionError):
            json.loads('{"servers":[],"servers":[]}', object_pairs_hook=validate.unique_object)


if __name__ == '__main__':
    unittest.main()
