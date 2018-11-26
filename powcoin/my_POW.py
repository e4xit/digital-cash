import hashlib
import time
import random

max_nonce = 2 ** 22  # 4 billion
# max_nonce = 2 ** 32  # 4 billion

# initial current_target for first period
initial_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

current_target = initial_target

# retarget interval
target_interval = 25

# in seconds
desired_block_time = 60

# initialise block times list for target calculation
block_times = []


def create_block_header(string, nonce):
    block_string = (str(string) + str(nonce))
    block_header = block_string.hex()
    print('block header: ', block_string)
    return block_header


def hash_block(block_header):
    headerByte = block_header.decode('hex')
    block_hash = hashlib.sha256(hashlib.sha256(headerByte).digest()).digest()
    block_hash.encode('hex_codec')
    print('block hash ', block_hash)
    return block_hash


def proof_of_work_block(target):

    for nonce in range(max_nonce):

        block_data = "this is only a test"
        block = create_block_header(block_data, nonce)
        block_hash = hash_block(block)
        print("target:     ", current_target)
        #print("target type: ", type(current_target))
        print("block hash: ", block_hash)
        #print("block_hash type: ", type(block_hash))

        if int(block_hash, 16) < target:
            print("Success with nonce %d" % nonce)
            print("Target was: ", current_target)
            print("Hash is %s" % block_hash)
            current_block += 1
            return block_hash, nonce

    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce


def calculate_avg_block_time():
    return sum(block_times[-target_interval:]) / target_interval


def set_target(block):

    avg_block_time = calculate_avg_block_time()

    print("current block number is: ", current_block)

    if block == 0:
        return current_target

    # blocks too fast
    elif avg_block_time < desired_block_time:
        new_target = current_target / (desired_block_time / avg_block_time)
        print("new target is: ", new_target)
        print("new_target is type ", type(new_target))
        return new_target

    # blocks too slow
    elif calculate_avg_block_time() > desired_block_time:
        new_target = current_target * (desired_block_time / avg_block_time)
        print("new_target is type ", type(new_target))
        print("new target is: ", new_target)

        return new_target

    # error
    else:
        return Exception


if __name__ == '__main__':

    current_block = 0

    print("Initial target is: ", initial_target)

    while current_block <= 100:

        if current_block % target_interval == 0 and current_block != 0:
            print("setting initial target")
            current_target = set_target(current_block)

        # checkpoint the current time
        start_time = time.time()

        proof_of_work_block(current_target)

        # checkpoint how long it took to find a result
        end_time = time.time()

        elapsed_time = end_time - start_time
        block_times.append(elapsed_time)
        print("Elapsed Time: %.4f seconds" % elapsed_time)

        # if elapsed_time > 0:
        #     # estimate the hashes per second
        #     hash_power = float(int(nonce) / elapsed_time)
        #     print("Hashing Power: %ld hashes per second" % hash_power)

        # current_block += 1


