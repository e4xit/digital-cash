##############
# Validation #
##############
import hashlib

import miner
import networking
import os
import my_logger
from utils import serialize

PORT = 10000


class Node:

    def __init__(self):
        self.blocks = []
        self.utxo_set = {}
        self.mempool = []
        self.peer_addresses = {(p, PORT) for p in os.environ.get('PEERS', '').split(',') if p}

    @property
    def mempool_outpoints(self):
        return [tx_in.outpoint for tx in self.mempool for tx_in in tx.tx_ins]

    def fetch_utxos(self, public_key):
        return [tx_out for tx_out in self.utxo_set.values()
                if tx_out.public_key == public_key]

    def update_utxo_set(self, tx):
        # Remove utxos that were just spent
        for tx_in in tx.tx_ins:
            del self.utxo_set[tx_in.outpoint]
        # Save utxos which were just created
        for tx_out in tx.tx_outs:
            self.utxo_set[tx_out.outpoint] = tx_out

    def fetch_balance(self, public_key):
        # Fetch utxos associated with this public key
        utxos = self.fetch_utxos(public_key)
        # Sum the amounts
        return sum([tx_out.amount for tx_out in utxos])

    def validate_tx(self, tx):
        in_sum = 0
        out_sum = 0
        for index, tx_in in enumerate(tx.tx_ins):
            # TxIn spending an unspent output
            assert tx_in.outpoint in self.utxo_set

            # No pending transactions spending this same output
            assert tx_in.outpoint not in self.mempool_outpoints

            # Grab the tx_out
            tx_out = self.utxo_set[tx_in.outpoint]

            # Verify signature using public key of TxOut we're spending
            public_key = tx_out.public_key
            tx.verify_input(index, public_key)

            # Sum up the total inputs
            amount = tx_out.amount
            in_sum += amount

        for tx_out in tx.tx_outs:
            # Sum up the total outputs
            out_sum += tx_out.amount

        # Check no value created or destroyed
        assert in_sum == out_sum

    def handle_tx(self, tx):
        self.validate_tx(tx)
        self.mempool.append(tx)

    # this one will only blow up if it fails
    def validate_block(self, block):
        assert block.proof < miner.POW_TARGET, "Insufficient Proof-of-Work"
        # check we are building on the tip of the chain
        assert block.prev_id == self.blocks[-1].id

    def handle_block(self, block):
        # check work, chain ordering
        self.validate_block(block)

        # Check the transactions are valid
        for tx in block.txns:
            self.validate_tx(tx)

        # If they're all good, update self.blocks and self.utxo_set
        for tx in block.txns:
            self.update_utxo_set(tx)

        # Add the block to our chain
        self.blocks.append(block)

        # now we have accepted the block so let's log it
        my_logger.logger.info(f"Block accepted: height={len(self.blocks) - 1}")

        # Block Propagation
        for peer_address in self.peer_addresses:
            networking.send_message(peer_address, "block", block)


class Block:

    # prev_id points to hex hash of previous block

    def __init__(self, txns, prev_id, nonce):
        self.txns = txns
        self.prev_id = prev_id
        self.nonce = nonce

    @property
    def header(self):
        return serialize(self)

        # this is the same as commented line below
        # return serialize([self.txns, self.prev_id])

    @property
    def id(self):
        return hashlib.sha256(self.header).hexdigest()

    @property
    def proof(self):
        return int(self.id, 16)

    def __repr__(self):
        return f"Block(prev_id={self.prev_id[:10]} id={self.id[:10]}...)"
