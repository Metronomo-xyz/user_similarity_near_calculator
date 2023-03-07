import pymongo
import time
import sys

class MongoWriter():
    def __init__(self, host = "127.0.0.1", port = 27017):
        timeout = 5000
        self.client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=timeout)
        try:
            result = self.client.admin.command("ismaster")
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Server did not managed to set connection in " + (str(timeout/1000)) + " seconde. Liekly that server is unavailable")
            raise ValueError("Can't establish connection. Wrong host or/and port : " + host + ":" + str(port))

    def writeSimilarityToCollection(self, similarity, database, collection):
        db = self.client[database]
        collection = db[collection]
        wallet_set = set([s[0] for s in similarity])

        print("Creating document to write to mongo. Can take a while.")
        # TODO: poor performance, need to optimize
        tm0 = time.time()
        json_data = [{"wallet_1": str(e), "similarities": [{"wallet_2": str(s[1]), "similarity": str(s[2])} for s in similarity if s[0] == e]} for e in set(wallet_set)]
        tm1 = time.time()
        print("Document creation took : " + str(tm1-tm0))
        try:
            tm0 = time.time()
            responces = collection.insert_many(json_data)
            tm1 = time.time()
        except Exception as e:
            print(e)
            sys.exit(1)

        print("Similarity is written to the MongoDB : " + str(self.client.HOST) + "." + str(db.name) + "." + str(collection.name))
        print("Mongo insert took " + str(tm1 - tm0) + " seconds")