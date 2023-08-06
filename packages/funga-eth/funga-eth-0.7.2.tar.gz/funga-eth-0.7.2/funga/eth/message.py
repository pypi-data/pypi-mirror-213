# external imports
import sha3
import logging

# local imports
from .encoding import to_checksum_address

logg = logging.getLogger(__name__)

def to_digest(data):
    h = sha3.keccak_256()
    h.update(data)
    return h.digest()

# ERC191 - version 0x00
def to_validator_message(data, validator, digest=False):
    a = to_checksum_address(validator)
    v = bytes.fromhex(a)
    r = b'\x19\x00' + v + data
    logg.debug('raw message data: ' + r.hex())
    if digest:
        r = to_digest(r)
    return r


# ERC191/ERC712 - version 0x01
def to_typed_message(data, domain, digest=False):
    assert len(data) == 32
    assert len(domain) == 32
    r = b'\x19\x01' + domain + data
    logg.debug('raw message data: ' + r.hex())
    if digest:
        r = to_digest(r)
    return r


# ERC191 - version 0x45
def to_personal_message(data, digest=False):
    ethereumed_message_header = b'\x19\x45' + 'thereum Signed Message:\n{}'.format(len(data)).encode('utf-8')
    r = ethereumed_message_header + data
    logg.debug('raw message data: ' + r.hex())
    if digest:
        r = to_digest(r)
    return r



