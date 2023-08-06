#!/usr/bin/python

# standard imports
import unittest
import logging
import base64
import os

# external imports
from hexathon import (
    strip_0x,
    add_0x,
)

# local imports
from funga.error import UnknownAccountError
from funga.eth.keystore.dict import DictKeystore
from funga.eth.signer import EIP155Signer

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.realpath(os.path.dirname(__file__))


class TestDict(unittest.TestCase):
    address_hex = None
    db = None

    def setUp(self):
        self.db = DictKeystore()

        keystore_filepath = os.path.join(script_dir, 'testdata',
                                         'UTC--2022-01-24T10-34-04Z--cc47ad90-71a0-7fbe-0224-63326e27263a')

        address_hex = self.db.import_keystore_file(keystore_filepath, 'test')
        self.address_hex = add_0x(address_hex)

    def tearDown(self):
        pass

    def test_get_key(self):
        logg.debug('getting {}'.format(strip_0x(self.address_hex)))
        pk = self.db.get(strip_0x(self.address_hex), '')

        self.assertEqual(self.address_hex.lower(), '0xb8df77e1b4fa142e83bf9706f66fd76ad2a564f8')

        bogus_account = os.urandom(20).hex()
        with self.assertRaises(UnknownAccountError):
            self.db.get(bogus_account, '')

    def test_sign_message(self):
        s = EIP155Signer(self.db)
        z = s.sign_ethereum_message(strip_0x(self.address_hex), b'foo')
        logg.debug('zzz {}'.format(str(z)))


if __name__ == '__main__':
    unittest.main()
