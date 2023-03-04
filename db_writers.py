import pymongo
import time

class MongoWriter():
    def __init__(self, host = "127.0.0.1", port = 27017):
        self.client = pymongo.MongoClient(host=host, port=port)

    def writeSimilarityToCollection(self, similarity, database, collection):
        db = self.client[database]
        collection = db[collection]

        wallet_set = set([s[0] for s in similarity])

        json_data = [{"wallet_1": str(e), "similarities": [{"wallet_2": str(s[1]), "similarity": str(s[2])} for s in similarity if s[0] == e]} for e in set(wallet_set)]

        try:
            tm0 = time.time()
            responces = collection.insert_many(json_data)
            tm1 = time.time()
        except Exception as e:
            print(e)

        print("Similarity is written to the MongoDB : " + str(self.client.HOST) + "." + str(db.name) + "." + str(collection.name))
        print("Mongo insert took " + str(tm1 - tm0) + " seconds")