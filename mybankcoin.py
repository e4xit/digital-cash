from ecdsa import SigningKey, SECP256k1
from utils import serialize
from copy import deepcopy
from uuid import uuid4


## because this is now a centralized coin we can now delete these as whatever the bank says goes

# bank_private_key = SigningKey.generate(curve=SECP256k1)
# bank_public_key = bank_private_key.get_verifying_key()


def transfer_message(previous_signature, public_key):
    return serialize({
        "previous_signature": previous_signature,
        "next_owner_public_key": public_key,
    })


class Transfer:
    
    def __init__(self, signature, public_key):
        self.signature = signature
        self.public_key = public_key

    def __eq__(self, other):
        return self.signature == other.signature and self.public_key.to_string() == other.public_key.to_string()


class BankCoin:
    
    def __init__(self, transfers):
        self.id = uuid4()
        self.transfers = transfers

    def __eq__(self, other):
        return self.id == other.id and self.transfers == other.transfers


    def validate(self):
        # Check the subsequent transfers
        previous_transfer = self.transfers[0]
        for transfer in self.transfers[1:]:
            # Check previous owner signed this transfer using their private key
            assert previous_transfer.public_key.verify(
                transfer.signature,
                transfer_message(previous_transfer.signature, transfer.public_key),

            )
            previous_transfer = transfer

    def transfer(self, owner_private_key, recipient_public_key):
        previous_signature = self.transfers[-1].signature
        message = transfer_message(previous_signature, recipient_public_key)
        transfer = Transfer(
            signature=owner_private_key.sign(message),
            public_key=recipient_public_key
        )
        self.transfers.append(transfer)


class Bank:

    # mapping of coin.id -> coin
    # if you give ID of a coin you can look it up
    def __init__(self):
        # make a new blank dictionary to store values in
        self.coins = {}

    def issue(self, public_key):
        transfer = Transfer(
        # as we now trust the bank:
            signature=None,
            public_key=public_key,
        )

        # Create and return the coin with just the issuing transfer
        coin = BankCoin(transfers=[transfer])

        # put the coin into the bank database
        # use a deepcopy here so that python won't accidentally modify bank database coin
        self.coins[coin.id] = deepcopy(coin)

        return coin

    # check coins in banks database
    def fetch_coins(self, public_key):
        coins = []
        # we loop through transfers as that's where the public keys are
        for coin in self.coins.values():
            if coin.transfers[-1].public_key.to_string() == public_key.to_string():
                coins.append(coin)
        return coins

    def observe_coin(self, coin):
        last_observation = self.coins[coin.id]
        last_observation_num_transfers = len(last_observation.transfers)

        assert last_observation.transfers == \
               coin.transfers[:last_observation_num_transfers]

        coin.validate()

        self.coins[coin.id] = deepcopy(coin)

        return coin