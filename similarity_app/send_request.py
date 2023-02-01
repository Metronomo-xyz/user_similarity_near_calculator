#from flask import request
import requests


if __name__=='__main__':
#    files = {"similarity":open('../similarity.csv', "rb")}
    params={"bucket":"near-data",
           "path":"similarity_data/similarity.csv",
            "local":True}
    r = requests.get('http://127.0.0.1:5000/load_similarity/', params=params)
    print(r.text)

