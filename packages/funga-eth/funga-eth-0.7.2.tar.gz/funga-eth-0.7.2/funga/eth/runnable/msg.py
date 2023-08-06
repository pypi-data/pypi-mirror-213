# standard imports
import os
import logging
import sys
import json
import argparse
import getpass

# external impors
import coincurve
from hexathon import strip_0x

# local imports
from funga.error import DecryptError
from funga.eth.keystore.dict import DictKeystore
from funga.eth.signer import EIP155Signer


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argparser = argparse.ArgumentParser()
argparser.add_argument('-f', type=str, help='Keyfile to use for signing')
argparser.add_argument('-z', action='store_true', help='zero-length password')
argparser.add_argument('-v', action='store_true', help='be verbose')
argparser.add_argument('-0', dest='nonl', action='store_true', help='no newline at end of output')
argparser.add_argument('-b', '--binary', dest='binary', action='store_true', help='parse input as binary hex')
argparser.add_argument('--validator', type=str, help='if set, will sign an ERC191 version 0 message')
argparser.add_argument('msg', type=str, help='Message to sign')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)


def main():
    passphrase = os.environ.get('WALLET_PASSPHRASE', os.environ.get('PASSPHRASE'))
    if args.z:
        passphrase = ''
    if passphrase == None:
        passphrase = getpass.getpass('decryption phrase: ')
   
    keystore = DictKeystore()
    address = keystore.import_keystore_file(args.f, password=passphrase)

    signer = EIP155Signer(keystore)

    msg = None
    if args.binary:
        hx = strip_0x(args.msg, pad=True)
        msg = bytes.fromhex(hx)
    else:
        msg = args.msg.encode('utf-8').hex()

    sig = None
    if args.validator:
        logg.info('signing validator message (ERC191 version 0)')
        sig = signer.sign_validator_message(address, args.validator, msg, password=passphrase)
    else:
        logg.info('signing personal message (ERC191 version 0x45)')
        sig = signer.sign_ethereum_message(address, msg, password=passphrase)

    r = sig.hex()
    if not args.nonl:
        r += "\n"
    sys.stdout.write(r)


if __name__ == '__main__':
    main()
