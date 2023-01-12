import io
from uuid import uuid4


CLIENT_ID_POOL = []


def generate_client_id() -> str:
    """Unique id generator uuid4 from RFC 4122"""
    client_id = str(uuid4()).encode()
    CLIENT_ID_POOL.append(client_id)
    return client_id


async def remove_client_id(client_id: bytes):
    CLIENT_ID_POOL.remove(client_id)
