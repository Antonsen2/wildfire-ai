from dotenv import dotenv_values


def get_encryption_key():
    env = dotenv_values(".env")
    return env['ENCRYPTION_KEY']
