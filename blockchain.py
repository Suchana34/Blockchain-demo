# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 02:38:07 2019

@author: SUCHANA CHAKRABARTI
"""

#creating  a blockchain
import datetime
import hashlib
import json
from flask import Flask, jsonify

#building our blockchain
class Blockchain():
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
    
        return new_proof
    # we r going to hash a block using sha256
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # now to check if the prev hash of this block is equal to the hash of the prev block
            if block['previous_hash']  != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
    # now we will check proof of the prev and the currrent block starts with 4 leading zeroes
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    # thus now we have a hashing algorithm vteween the proofs
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

            
# creating webapp
app = Flask(__name__)
#creating a blockchain

blockchain = Blockchain() #instance of our class


# mining our blockchain
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'congrats..you just mined a blockchain',
                'index' : block['index'],
                'timestamp': block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

#getting the full blockchain
@app.route('/get_fullchain', methods = ['GET'])
def get_fullchain():
    response ={'chain' : blockchain.chain,
               'length' : len(blockchain.chain)}
    return jsonify(response), 200 

#running the app
app.run(host = '0.0.0.0' , port = 5000)











