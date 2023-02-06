# user_similarity_near_calculator
Tool to calculate users similarity on NEAR blockchain

It's part of user_similarity_near functionality

![architecture](http://dl3.joxi.net/drive/2023/02/06/0016/0232/1081576/76/0a35919c3e.jpg)

This module calculates users similarity based on transactions data and stores it in provided Google Cloud Storage blob.

After that, you can load this similarity data into user_similarity_near_app and request similarities from it.

Be aware, that calculation of similarity with popular smart contract will lead to $O(n^2)$ memory consumption. Therefore, highly recommended removing from analysis smart contract, which has very large number of users.

Also, it's reasonable from the gained information perspective: if some smart contract (i.e. `wrap.near`) is used by almost every participant in the network, then there is no new and useful information that wallet interacted with `wrap.near` in terms of determining wallet behaviour and interests.

Module uses some data cleaning steps:
- removing smart contract, which has the largest number of users from the analysis. See `removeContractsPercentile` variable in `config.py` 
- removing some hardcoded list of smart-contract from analysis. See `removeContracts` variable in `config.py`
- removing users with high number of interactions (mostly bots) from analysis. See `removeWalletsPercentile` variable in `config.py`

Because of percentile cleaning usage it might be, that taking shorted data period will lead to increase in memory consumption.
It happens, because on a short period of time popular smart contracts are not so divided from other in number of interactions. Therefore, they are not cleaned from analysis by 99-th percentile cut.

## Prerequisites

### Hardware
The main bottleneck of current module is RAM, so at least 16GB of RAM needed.


### Data source
Either you can use provided public transactions data or use your own data connector. 

To use public data you have to
1. pass `-p` option while running 
2. Create google auth default credentials. More detail [below](#3-create-google-auth-default-credentials)

To use your own data connector you have to implement DataConnector abstract class and provided some setting in config file (if needed). 
### Create Google cloud storage bucket
To store similarity data now there is only connector to google storage bucket. Therefore, you need to create one and provide config.py with bucket name, blob path and json key

[Here you can find details on how to create bucket](https://cloud.google.com/storage/docs/discover-object-storage-console#create_a_bucket)

### Change config.py

As said above you need to provide bucket name, blob path and json key file to the module via config.py file.

1. `SIMILARITY_BUCKET = <name of your bucket>` - bucket to use to store the similarity data. It's also possible to provide json key file with `-b` or `--similarity_bucket` option instead of changing config
2. `SIMILARITY_BLOB = <path and mane of the blob>` - blob to store similarity bucket. No need to create blob upfront, it will be created (or replaced) while running the module. It's also possible to provide json key file with `-l` or `--similarity_blob` option instead of changing config
3. `SIMILARITY_BUCKET_TOKEN_JSON_PATH = <json key file>` - json key which will be used to get access to the bucket. Currently, only token json authentication is supported. [More detail on how to create json key file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). It's also possible to provide json key file with `-t` or `--similarity_token_json_path` option instead of changing config

## Running

### 0. Clone repository

`git clone https://github.com/Metronomo-xyz/user_similarity_near_calculator.git`

### 1. Create virtual environment

It's recommended to use virtual environment while using module

If you don't have `venv` installed run (ex. for Ubuntu)
```
sudo apt-get install python3-venv

```
then create and activate virtual environment
```
python3 -m venv simcalc_near
source simcalc_near/bin/activate
```

### 2. Install requirements
Run
```
pip install -r user_similarity_near_calculator/requirements.txt
```
### 3. Create google auth default credentials
These credentials needed to access Google Cloud Storage data with public NEAR tx data from Metronomo
The easiest method is to run

```gcloud auth application-default login --no-launch-browser```

and then copy authentication link to browser and then copy code from browser to shell.

For other ways to create credentials see

[https://cloud.google.com/docs/authentication/provide-credentials-adc](https://cloud.google.com/docs/authentication/provide-credentials-adc)

### 4. Run the module

```python3 -m user_similarity_near_calculator -p -s 31012023 -r 30```

### 5. Possible options:

- `-p`, `--public-data` to use module with public data
- `-s`, `--start_date` the last date of the dates period in `ddmmyyyy` format
- `-r`, `--date_range` number of days to take into power users calculation. For example, if start date is 12122022 and range 30 then dates will be since 13-11-2022 to 12-12-2022 inclusively
- `-b`, `--similarity_bucket` - bucket to use to store the similarity data.
- `-l`, `--similarity_blob` - blob to store similarity bucket. No need to create blob upfront, it will be created (or replaced) while running the module.
- `-d`, `--similarity_token_json_path` - json key which will be used to get access to the bucket. Currently, only token json authentication is supported. [More detail on how to create json key file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).