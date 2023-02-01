"""
Config file with constants and other configutrations for your data connectors
All the constants related to specific connectors have name of the connector in the constant name
"""
""""""
MetronomoTXCloudStorageConnector_DEFAULT_NETWORK = "mainnet"
MetronomoTXCloudStorageConnector_DEFAULT_BUCKET_NAME = "near-data"
MetronomoTXCloudStorageConnector_DEFAULT_GRANULARITY = "daily"
MetronomoTXCloudStorageConnector_TOKEN_JSON_PATH = '../../web3advertisement-b54340ad58ad.json'
MetronomoTXCloudStorageConnector_LOCAL_TOKEN_JSON_PATH = 'C:/Users/yaroslav/Documents/JupyterNotebooks/web3advertisement-b54340ad58ad.json'
MetronomoTXCloudStorageConnector_LOCAL_TEST_JSON_WITHOUT_KEY = 'C:/Users/yaroslav/Documents/Metronomo/power_users/test_json_without_key.json'
MetronomoTXCloudStorageConnector_LOCAL_TEST_JSON_WITH_NO_PERMISSIONS = 'C:/Users/yaroslav/Documents/Metronomo/power_users/web3advertisement-0a5600f53222.json'


MetronomoTXCloudStorageConnector_ENTITIES = {
    "transactions" : {
        "fields": ["signer_account_id", "receiver_account_id", "converted_into_receipt_id"],
        "files_part" : "transactions"
    },
    "actions" : {
        "fields": ["receipt_id", "action_kind"],
        "files_part" : "actionreceiptactions"
    }
}

MetronomoTXCloudStorageConnector_BLOB_PATHS = {
    "mainnet": {
        "hourly": {
            "transactions" : "mainnet/hourly_data/transactions/",
            "actions" : "mainnet/hourly_data/action_receipt_actions/"
        },
        "monthly" : {
            "transactions" : "mainnet/monthly_data/transactions/",
            "actions" : "mainnet/monthly_data/action_receipt_actions/"
        },
        "daily": {
            "transactions": "mainnet/daily_data/transactions/",
            "actions": "mainnet/daily_data/action_receipt_actions/"
        }
    },
    "testnet" : {
        "hourly": {
            "transactions": "testnet/hourly_data/transactions/",
            "actions": "testnet/hourly_data/action_receipt_actions/"
        },
        "monthly": {
            "transactions": "testnet/monthly_data/transactions/",
            "actions": "testnet/monthly_data/action_receipt_actions/"
        }
    }
}

removeContracts = {"near", "wrap.near", "aurora"}
removeContractsPercentile = 99.9
removeWalletsPercentile = 99
