from abc import ABC, abstractmethod
import pandas as pd
from similarity_calculator import config as c
from similarity_calculator import google_cloud_storage_utils as csu
from google.cloud import storage


class DataConnector(ABC):
    @abstractmethod
    def getData(self) -> pd.DataFrame:
        pass

class MetronomoTXCloudStorageConnector(DataConnector):

    # this variabel stores some Metronomo.xyz Google Cloud Storage blobs structure to generalize access
    # to possible different datasets

    ENTITIES = {
        "transactions": {
            "fields": ["signer_account_id", "receiver_account_id", "converted_into_receipt_id"],
        },
        "actions": {
            "fields": ["receipt_id"],
        }
    }

    BLOB_PATHS = {
        "mainnet": {
            "daily": {
                "transactions": "mainnet/daily_data/transactions/",
                "actions": "mainnet/daily_data/action_receipt_actions/"
            }
        }
    }

    # This class implements DataConnector class
    # and incapsulates the logic to retrieve TX data from
    # Metronomno.xyz Google Cloud Storage

    # Current implementation will NOT be useful for anyone who wants to use power_users tool
    # However if you use data from your own Google Cloud Storage it is possible to adjust the code to your needs

    # The main source of data below was NEAR Indexer for Explorer PostgresSQL database
    # https://github.com/near/near-indexer-for-explorer
    # We get transactions table once a day for previous day in a hourly batches.
    # Then we combine hourly batches into one daily batch

    # MetronomoTXCloudStorageConnector stores some data structure for Metronomno.xyz Google Cloud Storage data
    # for using in Power Users module

    def __init__(self,
                 dates,
                 bucket_name,
                 network,
                 with_public_data = False,
                 token_json_path=None,
                 granularity=c.MetronomoTXCloudStorageConnector_DEFAULT_GRANULARITY):
        """
        Parameters
        ----------
        dates: list[datetime.Date]
            dates range to retrieve the data. Should be iterable of datetime.date type
        run_local: str
            flag to run code locally (priority higher than token_json_path). In case of local running path for local toke_json file is used
        bucket_name: str
            name of the bucket to get data from. Either provided or got from config.py file, variable MetronomoTXCloudStorageConnector_DEFAULT_BUCKET_NAME
        token_json_path: str
            path to token json file. Either provided or got from config.py file, variable MetronomoTXCloudStorageConnector_TOKEN_JSON_PATH
        network:
            network to get data from. Currently, possible only "mainnet" data
        granularity:
            data granularity to retrive. Currently possible only "daily" data
        """

        self.with_public_data = with_public_data
        print("with public data : " + str(self.with_public_data))
        if (self.with_public_data):
            self.token_json_path = None
            self.storage_client = storage.Client(project=c.MetronomoTXCloudStorageConnector_DEFAULT_PROJECT)

        else:
            self.token_json_path = token_json_path
            self.storage_client = storage.Client.from_service_account_json(self.token_json_path)

        self.bucket_name = bucket_name
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

        if not (network  in self.BLOB_PATHS.keys()):
            raise ValueError("Wrong network provideded : " + network + ". Network not in BLOB_PATHS. Please choose correct network : " + ", ".join(map(str, self.BLOB_PATHS.keys())))
        if not (network in set(map(lambda x: x.name.split("/")[0], list(self.bucket.list_blobs())))):
            raise ValueError("Wrong network provideded : " + network + ". Network not in bucket")

        self.network = network
        self.dates = dates
        self.granularity = granularity

    def __str__(self):
        return "CloudStorageConnectror object : " + "\n" + \
               "bucket_name : " + str(self.bucket_name) + "\n" + \
               "token_json_path : " + str(self.token_json_path) + "\n" + \
               "storage_client : " + str(self.storage_client) + "\n" + \
               "bucket : " + str(self.bucket) + "\n" + \
               "network : " + str(self.network) + "\n" + \
               "dates : " + str(self.dates) + "\n" + \
               "granularity : " + str(self.granularity)

    def getData(self):
        all_blobs = csu.get_blob_list(self.storage_client, self.bucket)
        tx_blobs = csu.filter_blobs_by_path(
            all_blobs,
            self.BLOB_PATHS[self.network][self.granularity]["transactions"],
        )
        tx_blobs = csu.filter_blobs_by_dates(tx_blobs, self.dates)
        print("tx_blobs : ")
        print(tx_blobs)
        if (len(tx_blobs)==0):
            raise ValueError("List of blobs with tx data is empty. Check that data for provided start_date/date_range exists in the storage.")

        tx_df = pd.DataFrame()
        for tx_b in tx_blobs:
            print("current blob : ")
            print(tx_b)
            tx_data = csu.get_dataframe_from_blob(
                self.bucket,
                tx_b,
                self.token_json_path,
                self.ENTITIES["transactions"]["fields"]
            )
            tx_data = tx_data[self.ENTITIES["transactions"]["fields"]]
            tx_df = pd.concat([tx_df, tx_data])
        tx_df = tx_df.drop_duplicates()


        ara_blobs = csu.filter_blobs_by_path(
            all_blobs,
            self.BLOB_PATHS[self.network][self.granularity]["actions"],
        )
        ara_blobs = csu.filter_blobs_by_dates(ara_blobs, self.dates)
        print("ara_blobs : ")
        print(ara_blobs)

        ara_df = pd.DataFrame()
        for ara_b in ara_blobs:
            print("current blob : ")
            print(ara_b)
            ara_data = csu.get_dataframe_from_blob(
                self.bucket,
                ara_b,
                self.token_json_path,
                self.ENTITIES["actions"]["fields"]
            )
            ara_data = ara_data[self.ENTITIES["actions"]["fields"]]
            ara_df = pd.concat([ara_df, ara_data])
        ara_df = ara_df.drop_duplicates()

        data = tx_df.set_index("converted_into_receipt_id").join(ara_df.set_index("receipt_id"),how = "inner")
        data = data.reset_index().groupby(["signer_account_id", "receiver_account_id"]).count().reset_index()
        data.columns = ["signer_account_id", "receiver_account_id", "interactions_num"]
        return data