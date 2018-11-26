#!/usr/bin/env python
# example of proof-of-work algorithm to create 1 min blocks on your system

import hashlib
import time


max_nonce = 2 ** 32  # 4 billion

# initial current_target for first period
current_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

# largest possible allowed target
difficulty_1_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

# difficulty is largest possible target divided by the current target
difficulty = difficulty_1_target / current_target

# retarget interval
target_interval = 25

# in seconds
desired_block_time = 60

# initialise block times list for target calculation
block_times = []


def proof_of_work(header, current_target):

    for nonce in range(max_nonce):
        hash_string = (str(header) + str(nonce)).encode()
        hash_result = hashlib.sha256(hash_string).hexdigest()

        # check if this is a valid result, below the target
        if int(hash_result, 16) < current_target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result)
            return (hash_result, nonce)

    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce

def calculate_avg_block_time():
    if current_block % target_interval == 0:
        avg_block_time = (sum(block_times[-target_interval:]) / target_interval)
        return avg_block_time

if __name__ == '__main__':
    nonce = 0
    hash_result = ''

#     # set range
    # #     for target in range(difficulty_1_target, 0):
    # #         print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))
    # #         print("Starting search...")

    current_block = 0

    while current_block < 1000:

        # checkpoint the current time
        start_time = time.time()

        # make a new block which includes the hash from the previous block
        # we fake a block of transactions - just a string
        new_block = 'test block with transactions' + hash_result

        # find a valid nonce for the new block
        (hash_result, nonce) = proof_of_work(new_block, current_target)

        # checkpoint how long it took to find a result
        end_time = time.time()

        elapsed_time = end_time - start_time
        print("Elapsed Time: %.4f seconds" % elapsed_time)
        block_times.append(elapsed_time)

        if elapsed_time > 0:
            # estimate the hashes per second
            hash_power = float(int(nonce) / elapsed_time)
            print("Hashing Power: %ld hashes per second" % hash_power)

        current_block =+ 1

        calculate_avg_block_time()

        if avg_block_time > (target_interval * desired_block_time):
            reduce_target()
        elif avg




