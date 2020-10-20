import os
import pymongo
import pickledb

from .data_processing import get_app_path


def test_connection(mdb_url, maxServDelay=2000):
    try:
        testClient = pymongo.MongoClient(mdb_url, serverSelectionTimeoutMS=maxServDelay)
        testClient.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
        return 0

    return 1


def upload_output(data):
    print("Saving on MongoDB...")

    app_path = get_app_path()
    configs_db = pickledb.load(os.path.join(app_path, "configs.json"), False)

    mdb_url = configs_db.get("mongoDB_URL")
    if test_connection(mdb_url):
        mongo_client = pymongo.MongoClient(mdb_url)

        capiDB = mongo_client["capi"]
        stats_collection = capiDB["statistics"]
        stats_collection.insert_one(data[0])

        recs_collection = capiDB["recommendations"]
        recs_collection.insert_one(data[1])

        mongo_client.close()
        return 1
    else:
        return 0
