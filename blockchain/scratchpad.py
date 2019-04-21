import hashlib


def valid_proof(last_proof, proof):
    """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    print(proof)


proof_of_work(24348)
