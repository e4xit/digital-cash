"""
BlockCoin

Usage:
  my_pow_syndacoin.py serve
  my_pow_syndacoin.py ping [--node <node>]
  my_pow_syndacoin.py tx <from> <to> <amount> [--node <node>]
  my_pow_syndacoin.py balance <name> [--node <node>]

Options:
  -h --help      Show this screen.
  --node=<node>  Hostname of node [default: node0]
"""

import threading
import miner
import wallet
import networking
import globalconfig

from docopt import docopt
from identities import user_private_key, user_public_key


#########
#  CLI  #
#########


def main(args):
    if args["serve"]:
        # spin up a new node in the global space to be shared
        # allows sharing between the threads

        # TODO: mine a genesis block
        miner.mine_genesis_block()

        # Start server thread
        server_thread = threading.Thread(target=networking.serve, name="server")
        server_thread.start()

        # Start miner thread
        miner_thread = threading.Thread(target=miner.mine_forever, name="miner")
        miner_thread.start()

    elif args["ping"]:
        address = address_from_host(args["--node"])
        networking.send_message(address, "ping", "")
    elif args["balance"]:
        public_key = user_public_key(args["<name>"])
        address = networking.external_address(args["--node"])
        response = networking.send_message(address, "balance", public_key, response=True)
        print(response["data"])
    elif args["tx"]:
        # Grab parameters
        sender_private_key = user_private_key(args["<from>"])
        sender_public_key = sender_private_key.get_verifying_key()
        recipient_private_key = user_private_key(args["<to>"])
        recipient_public_key = recipient_private_key.get_verifying_key()
        amount = int(args["<amount>"])
        address = networking.external_address(args["--node"])

        # Fetch utxos available to spend
        response = networking.send_message(address, "utxos", sender_public_key, response=True)
        utxos = response["data"]

        # Prepare transaction
        tx = wallet.prepare_simple_tx(utxos, sender_private_key, recipient_public_key, amount)

        # send to node
        networking.send_message(address, "tx", tx)
    else:
        print("Invalid command")


if __name__ == '__main__':
    main(docopt(__doc__))
