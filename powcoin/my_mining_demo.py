import hashlib
import time


def get_proof(header, nonce):
    preimage = f"{header}:{nonce}".encode()
    proof_hex = hashlib.sha256(preimage).hexdigest()
    return int(proof_hex, 16)


def mine(header, target, nonce):
    # take target as input, cycles through nonces until target is hit
    nonce = 0
    while get_proof(header, nonce) >= target:
        nonce += 1  # new guess
    return nonce


def mining_demo(header):
    previous_nonce = 0
    for difficulty_bits in range(1, 30):
        target = 2 ** (256 - difficulty_bits)
        # target_bin = format(target, '#0256b')

        start_time = time.time()
        nonce = mine(header, target, previous_nonce)
        proof = get_proof(header, nonce)
        elapsed_time = time.time() - start_time

        target_str = f"{target:.0e}"
        elapsed_time_str = f"{elapsed_time:.0e}" if nonce != previous_nonce else ""
        bin_proof_str = f"{proof:0256b}"[:50]

        print(
            f"bits: {difficulty_bits:>3} target: {target_str:>7} elapsed: {elapsed_time_str:>7} nonce: {nonce:>10} proof: {bin_proof_str}...")


if __name__ == "__main__":
    header = "hello"
    mining_demo(header)
