import jwt
import os


class Cryptography():
    def encode(payload):
        return jwt.encode(payload, os.getenv("SECRET"), os.getenv("ALGORITHM"))

    def decode(hash):
        return jwt.decode(hash, os.getenv("SECRET"), algorithms=os.getenv("ALGORITHM"))
