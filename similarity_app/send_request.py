#from flask import request
import requests


if __name__=='__main__':
    params={"bucket":"near-data",
           "path":"similarity_data/similarity.csv",
           "local":False}
    r = requests.get('http://127.0.0.1:5000/load_similarity/', params=params)
    files = {"file":open("wallets2.csv", 'rb')}
    r = requests.post('http://127.0.0.1:5000/similarity/csv', files=files)
    print(r.text)

