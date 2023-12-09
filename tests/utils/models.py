import secrets


def make_resource_id():
    return secrets.randbelow(1000000)
