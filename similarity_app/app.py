from flask import Flask, request
import config as c
import google_cloud_storage_utils as csu

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

    global similarity_matrix

    result = []
    for w in wallets_list:
        result = result + list(filter(lambda x: get_similarity_by_wallet(w), similarity_matrix))
    return ",".join(result)

@app.route("/load_similarity/", methods=['GET'])
def load_similarity():
    if request.method == 'GET':
        args = request.args
        print(args.keys())
        print(args["path"])
        print(args["bucket"])
        print(args["local"])

    if (args["local"]):
        token_json_path = c.MetronomoTXCloudStorageConnector_LOCAL_TOKEN_JSON_PATH

    bucket_name = args["bucket"]
    bucket = csu.get_bucket(token_json_path, bucket_name)

    global similarity_matrix

    print("similarity matrix: ")
    print(similarity_matrix)

    tmp = csu.get_dataframe_from_blob(bucket, args["path"], token_json_path, fields=None)
    similarity_matrix = tmp
    del tmp

    print("updated similarity matrix")
    print(similarity_matrix)
    return "well done!"