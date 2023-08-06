# funga-eth

Ethereum implementation of the `funga` signer interface.

See https://git.defalsify.org/funga for more details.

## Tools

When installed as a python package, three tools are installed in the python executable script path.

* `funga-ethd` - Signer daemon (see below for details).
* `eth-keyfile` - Ethereum keyfile en- and decoder, and en- and decrypter.
* `eth-msg-sign` - Signer tool for arbitrary messages ([ERC-191](https://eips.ethereum.org/EIPS/eip-191)).


### funga-ethd

A Unix socket IPC server as `funga-ethd` implementing the following web3 json-rpc methods:

* web3.eth.personal.newAccount
* web3.eth.personal.signTransaction
* web3.eth.signTransaction


### CLI tools

Please use `--help` as argument to the `eth-keyfile` and `eth-msg-sign` tools to learn the arguments the tools accept.


## Funga interface implementations

- **ReferenceKeystore**: Implements the `Keystore` interface, with a postgresql backend expecting sql schema as defined in `ReferenceKeystore.schema`
- **ReferenceSigner** Implements `Signer`, accepting a single argument of type `Keystore` interface. 
- **EIP155Transaction**: Creates transaction serializations appropriate for EIP155 replay protected signatures. Accepts a web3 format transaction dict as constructor argument together with nonce and optional chainId.
