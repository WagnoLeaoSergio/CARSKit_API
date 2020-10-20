import pymongo


def test_connection(mdb_url, maxServDelay=2000):
    try:
        testClient = pymongo.MongoClient(mdb_url,
                                         serverSelectionTimeoutMS=maxServDelay)
        testClient.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
        return 0

    return 1