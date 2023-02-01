from flask import Flask, request
import config as c
import google_cloud_storage_utils as csu
import time
import pandas as pd

similarity_matrix = []

app = Flask(__name__)

def get_similarity_by_wallet(x, wallet, lower_thershold=0.1, upper_thershold=1, default=False):
    try:
        return (x[1]==wallet) & (int(x[3]) >= lower_thershold) & (int(x[3]) <= upper_thershold)
    except (ValueError, TypeError):
        return default
    except:
        print(x)

@app.route("/similarity/csv", methods=['POST', 'GET'])
def get_similarity():
    if request.method == 'POST':
        file = request.files['file']
        wallets_list = file.read().decode().split("\r\n")
    print("wallet list : " + str(wallets_list))

    global similarity_matrix

    result = pd.DataFrame()
    for w in wallets_list:
        print(w)
        print("tmp : ")
        print(similarity_matrix[(similarity_matrix.iloc[:,0] == "zzzarathustra.near") & (similarity_matrix.iloc[:,2] >= 0.1) & (similarity_matrix.iloc[:,2] <= 1)].iloc[:,1])
        result = pd.concat([result, similarity_matrix[(similarity_matrix.iloc[:,0] == "zzzarathustra.near") & (similarity_matrix.iloc[:,2] >= 0.1) & (similarity_matrix.iloc[:,2] <= 1)].iloc[:,1]])
    result = result.drop_duplicates().iloc[:,0]
    print(type(result))
    print(result)
    return ",".join(result.to_list())

@app.route("/load_similarity/", methods=['GET'])
def load_similarity():
    if request.method == 'GET':
        args = request.args
        print(args.keys())
        print(args["path"])
        print(args["bucket"])
        print(args["local"])

    if (args["local"] == "True"):
        token_json_path = c.MetronomoTXCloudStorageConnector_LOCAL_TOKEN_JSON_PATH
        print("local path")
    else:
        print("server path")
        token_json_path = c.MetronomoTXCloudStorageConnector_TOKEN_JSON_PATH

    bucket_name = args["bucket"]
    bucket = csu.get_bucket(token_json_path, bucket_name)

    global similarity_matrix

    print("similarity matrix: ")
    print(similarity_matrix)

    start_time = time.time()
    tmp = csu.get_dataframe_from_blob(bucket, args["path"], token_json_path, fields=None)
    similarity_matrix = tmp
    del tmp
    print(time.time() - start_time)
    print("updated similarity matrix")
    print(similarity_matrix)
    return "well done!"
