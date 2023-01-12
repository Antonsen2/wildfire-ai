import asyncio
import socket
from aescipher import AESCipher
from settings import get_encryption_key
from prediction import model_predict, preprocess_image


AES = AESCipher(get_encryption_key())
HOST_SERVER = socket.gethostname()
PORT_SERVER = 5000
CHUNK_SIZE = 1024


async def run_server():
    server = await asyncio.start_server(handler, HOST_SERVER, PORT_SERVER)
    async with server:
        await server.serve_forever()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    init_data = await reader.read(CHUNK_SIZE)
    checksum, client_id = AES.decrypt(init_data.strip()).split()
    checksum = int(checksum)

    # recv image
    data = b''
    while not reader.at_eof():
        data += await reader.read(CHUNK_SIZE)

    # decrypt image
    data = AES.decrypt(data)

    # TODO verify checksum

    # prepare image for model
    image = preprocess_image(data)

    # use model
    fire_prediction = model_predict(image)

    # send back result
    msg = client_id + b" " + fire_prediction.encode("utf-8")
    checksum = f"{len(msg)}".encode("utf-8")
    msg = checksum + b" " + msg
    encrypted_msg = AES.encrypt(msg)
    response = encrypted_msg + b" " * (CHUNK_SIZE - len(encrypted_msg))

    writer.write(response)
    await writer.drain()

    writer.close()
    await writer.wait_closed()
