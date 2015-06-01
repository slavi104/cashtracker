import json
import requests
import os
from datetime import datetime

# for password hashing
import uuid
import hashlib

# Class with util functions
class Util():

    def currency_converter(curr_from, curr_to, curr_input):
        basepath = os.path.dirname(__file__)
        file_name = "{}.json".format(datetime.now().strftime('%Y_%m_%d'))
        rel_filepath = os.path.join(basepath, "..", "tmp", file_name)
        abs_filepath = os.path.abspath(rel_filepath)

        # if file exist so we already have current currencies
        if os.path.isfile(abs_filepath):
            with open(abs_filepath, "r") as f:
                exchange = json.loads(f.read())
        else:
            response = requests.get('http://api.fixer.io/latest')
            exchange = json.loads(response.content.decode())
            with open(abs_filepath, "w") as f:
                f.write(response.content.decode())

        rates = exchange['rates']

        return curr_input/rates.get(curr_from, 1)*rates.get(curr_to, 1)


    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))