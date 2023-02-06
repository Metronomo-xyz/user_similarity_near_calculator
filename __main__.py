import getopt
import sys
import datetime
from user_similarity_near_calculator import config as c
from user_similarity_near_calculator import events_data_connectors as dc
from user_similarity_near_calculator import similarity
import csv
from google.cloud import storage


if __name__ == '__main__':
    argv = sys.argv[1:]
    options = "ps:r:b:l:t:"
    long_options = ["public-data", "start_date=", "date_range=",\
                    "similarity_bucket=", "similarity_blob=", "similarity_token_json_path="]


    # interactions data source credentials
    with_public_data = False
    token_json_path = None

    # similarity storage destination
    similarity_bucket = c.SIMILARITY_BUCKET
    similarity_blob = c.SIMILARITY_BLOB
    similarity_bucket_token_json_path = c.SIMILARITY_BUCKET_TOKEN_JSON_PATH

    # other default parameters
    start_date = datetime.date.today() - datetime.timedelta(days=1)
    dates_range = 1
    removeContracts = c.removeContracts
    removeWalletsPercentile = c.removeWalletsPercentile
    removeContractsPercentile = c.removeContractsPercentile
    bucket_name = c.MetronomoTXCloudStorageConnector_DEFAULT_BUCKET_NAME
    network = c.MetronomoTXCloudStorageConnector_DEFAULT_NETWORK

    try:
        opts, args = getopt.getopt(argv, options, long_options)

        for opt, value in opts:
            if opt in ("-p", "--public-data"):
                with_public_data = True

            elif opt in ("-s", "--start_date"):
                try:
                    start_date = datetime.datetime.strptime(value, "%d%m%Y").date()
                except ValueError as e:
                    print("ERROR OCCURED: --start_date must be in %d%m%Y format, but " + value + " was given")
                    sys.exit(1)

            elif opt in ("-r", "--date_range"):
                try:
                    dates_range = int(value)
                except ValueError as e:
                    print("ERROR OCCURED: --date-range must be integer, but " + value + " was given")
                    sys.exit(1)

            elif opt in ("-b", "--similarity_bucket"):
                similarity_bucket = value

            elif opt in ("-l", "--similarity_blob"):
                similarity_bucket_token_json_path = value

            elif opt in ("-t", "--similarity_token_json_path"):
                bucket_name = value

    except getopt.GetoptError as e:
        print('Error while parsing command line arguments : ' + str(e))

    dates = [start_date - datetime.timedelta(days=x) for x in range(dates_range)]
    print(",".join([str(d) for d in dates]))
    gcs_connector = dc.MetronomoTXCloudStorageConnector(dates, with_public_data=with_public_data, bucket_name=bucket_name, network=network, token_json_path=token_json_path)
    data = gcs_connector.getData()

    row, col, similarity = similarity.calculateSimilarity(data, removeWalletsPercentile, removeContractsPercentile, removeContracts)

    storage_client = storage.Client.from_service_account_json(similarity_bucket_token_json_path)
    bucket = storage_client.get_bucket(similarity_bucket)
    blob = bucket.blob(similarity_blob)

    with blob.open("w") as f:
        writer = csv.writer(f)
        writer.writerows(zip(row, col, similarity))
    print("Similarity is written to the blob : " + "gs://" + similarity_bucket + "/" + similarity_blob)