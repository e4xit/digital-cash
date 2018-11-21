##########
# Mining #
##########


import threading
import random
import my_logger
import validation
import wallet
import globalconfig

DIFFICULTY_BITS = 20
POW_TARGET = 2 ** (256 - DIFFICULTY_BITS)
mining_interrupt = threading.Event()


def mine_block(block):
    while block.proof >= POW_TARGET:
        # TODO: accept interrupts if tip changes
        if mining_interrupt.is_set():
            my_logger.logger.info("Mining interrupted")
            mining_interrupt.clear()
            return
        block.nonce += 1
    return block


def mine_forever():
    my_logger.logging.info("Starting miner")
    while True:
        unmined_block = validation.Block(
            txns=globalconfig.node.mempool,
            prev_id=globalconfig.node.blocks[-1].id,
            nonce=random.randint(0, 100000000),

        )
        mined_block = mine_block(unmined_block)

        if mined_block:
            my_logger.logger.info("")
            my_logger.logger.info("Mined a block")
            globalconfig.node.handle_block(mined_block)


def mine_genesis_block():
    unmined_block = validation.Block(
        txns=[],
        prev_id=None,
        nonce=0,
    )

    mined_block = mine_block(unmined_block)
    globalconfig.node.blocks.append(mined_block)
    # TODO: update UTXO set, award coinbase, etc.
