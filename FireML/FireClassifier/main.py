import os
import asyncio
from Crypto import Random
from networking import run_server


def app():
    # GET hashicorp vault
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())


if __name__ == '__main__':
    app()
