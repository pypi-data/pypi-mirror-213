import os
import pymongo

MONGO_ADDRESS = os.environ["MONGO_ADDRESS"]
MONGO_PORT = os.environ["MONGO_PORT"]
MONGO_DB = os.environ["MONGO_DB"]
MONGO_USER_PATH = os.environ["MONGO_USER_PATH"]
MONGO_PASSWORD_PATH = os.environ["MONGO_PASSWORD_PATH"]


def get_creds():
    user, password = None, None
    with open(MONGO_USER_PATH, "r") as f:
        user = f.read().strip()

    with open(MONGO_PASSWORD_PATH, "r") as f:
        password = f.read().strip()

    return user, password


def connect():
    user, password = _get_creds()

    my_client = pymongo.MongoClient(
        host=MONGO_ADDRESS,
        port=int(MONGO_PORT),
        username=user,
        password=password,
        authSource=MONGO_DB,
    )

    print(my_client)

    return my_client[MONGO_DB]
