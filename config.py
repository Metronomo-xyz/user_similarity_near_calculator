"""
Config file with constants and other configutrations for your data connectors
All the constants related to specific connectors have name of the connector in the constant name
"""
""""""
MetronomoTXCloudStorageConnector_DEFAULT_PROJECT = "web3advertisement"
MetronomoTXCloudStorageConnector_DEFAULT_BUCKET_NAME = "near-data-public"
MetronomoTXCloudStorageConnector_DEFAULT_NETWORK = "mainnet"
MetronomoTXCloudStorageConnector_DEFAULT_GRANULARITY = "daily"

SIMILARITY_BUCKET = "near-data"
SIMILARITY_BLOB = "similarity_data/similarity.csv"
SIMILARITY_BUCKET_TOKEN_JSON_PATH = "web3advertisement-b54340ad58ad.json"

MetronomoTXCloudStorageConnector_ENTITIES = {
    "transactions" : {
        "fields": ["signer_account_id", "receiver_account_id", "converted_into_receipt_id"]
    },
    "actions" : {
        "fields": ["receipt_id", "action_kind"]
    }
}

MetronomoTXCloudStorageConnector_BLOB_PATHS = {
    "mainnet": {
        "hourly": {
            "transactions" : "mainnet/hourly_data/transactions/",
            "actions" : "mainnet/hourly_data/action_receipt_actions/"
        },
        "daily": {
            "transactions": "mainnet/daily_data/transactions/",
            "actions": "mainnet/daily_data/action_receipt_actions/"
        }
    }
}

removeContracts = {"near", "wrap.near", "aurora", "2260fac5e5542a773aa44fbcfedf7c193bc2c599.factory.bridge.near", "tge-lockup.sweat", "token.sweat"}
removeContractsPercentile = 99.9
removeWalletsPercentile = 99
