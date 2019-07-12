import hashlib
import requests
import json

import sys

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    if guess_hash[:6] == "000000":
        print(last_proof, proof, guess, guess_hash)
    return guess_hash[:6] == "000000"


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof



if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    last_proof = None
    while True:
        if last_proof == None:
            proof_request = requests.get(f'{node}/last_proof').json()
            last_proof = proof_request['last_proof']
        next_proof = proof_of_work(last_proof)
        answer = requests.post(f'{node}/mine', json={"proof": next_proof })
        if answer != None:
            answer = answer.json()
        else:
            # we messed up
            break
        if answer['message'] == 'New Block Forged':
            coins_mined += 1
            print(coins_mined)
            last_proof = next_proof
        else:
            last_proof = None

        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.

'''
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mine a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new BLock by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
'''