import os
import asyncio
from settings import get_encryption_key
from aescipher import AESCipher


AES = AESCipher(get_encryption_key())
HOST_FIREML = "fireml"
PORT_FIREML = 5000
CHUNK_SIZE = 1024


async def image_to_model(client_id: bytes, image) -> str:
    reader, writer = await asyncio.open_connection(HOST_FIREML, PORT_FIREML)

    # image header data
    checksum = f"{len(image)}".encode()
    header_data = AES.encrypt(checksum + b" " + client_id)
    header = header_data + b" " * (CHUNK_SIZE - len(header_data))

    writer.write(header)
    await writer.drain()

    writer.write(AES.encrypt(image))
    await writer.drain()
    writer.write_eof()

    response = await reader.read(CHUNK_SIZE)
    checksum, client_id, msg = AES.decrypt(response.strip()).split()

    return msg.decode()
