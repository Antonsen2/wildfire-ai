import os
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class AESCipher:
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, encode_data):
        encode_data = self.__pad(encode_data)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(encode_data)
        return b64encode(iv + encrypted_text)

    def decrypt(self, encrypted_data):
        encrypted_data = b64decode(encrypted_data)
        iv = encrypted_data[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        byte_data = cipher.decrypt(encrypted_data[self.block_size:])
        return self.__unpad(byte_data)

    def __pad(self, data):
        number_of_bytes_to_pad = self.block_size - len(data) % self.block_size
        ascii_byte = chr(number_of_bytes_to_pad).encode("utf-8")
        padding_bytes = number_of_bytes_to_pad * ascii_byte
        padded_data = data + padding_bytes
        return padded_data

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]
