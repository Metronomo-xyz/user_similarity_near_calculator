# user_similarity_near_calculator
Tool to calculate users similarity on NEAR blockchain

It's part of user_similarity_near functionality

![architecture](http://dl3.joxi.net/drive/2023/02/06/0016/0232/1081576/76/0a35919c3e.jpg)

This module calculates users similarity based on transactions data and stores it in provided Google Cloud Storage blob.

After that, you can load this similarity data into user_similarity_near_app and request similarities from it.


##Prerequisites
1. Either you can use provided public transactions data or use your own data connector. 
   1. To use public data you have to pass `-p` option while running
   2. Create google auth default credentials. More detail [below](#4-create-google-auth-default-credentials)
   3. To use your own data connector you have to implement DataConnector abstract class and provided some setting in config file (if needed).
2. Google cloud storage bucket
   1. [Details on how to create bucket](https://cloud.google.com/storage/docs/discover-object-storage-console#create_a_bucket)
3. Change config.py
   1. `SIMILARITY_BUCKET = <name of your bucket>` - bucket to use to store the similarity data
   2. `SIMILARITY_BLOB = <path and mane of the blob>` - blob to store similarity bucket. No need to create blob upfront, it will be created (or replaced) while running the module
   3. `SIMILARITY_BUCKET_TOKEN_JSON_PATH = <json key file>` - json key which will be used to get access to the bucket. Currently, only token json authentication is supported. [More detail on how to create json key file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)  

##Running
###2. Create virtual environment

It's recomended to use virtual environment while using module

If you don't have `venv` installed run (ex. for Ubuntu)
```
sudo apt-get install python3-venv

```
then create and activate virtual environment
```
python3 -m venv simcalc_near
source simcalc_near/bin/activate
```

### 3. Install requirements
Run
```
pip install -r simcalc_near/requirements.txt
```
### 4. Create google auth default credentials 
The easiest method is to run

```gcloud auth application-default login --no-launch-browser```

and then copy authentication link to browser and then copy code from browser to shell.

For other ways to create credentials see

[https://cloud.google.com/docs/authentication/provide-credentials-adc](https://cloud.google.com/docs/authentication/provide-credentials-adc)

### 5. Run the module

```python3 -m power_users -c voiceoftheoceans.mintbase1.near -p -s 31012023 -r 30```

### 6. Possible options:

- `-p`, `--public-data` to use module with public data
- `-n`, `--netowrk` to choose NEAR network. Currently, only `mainnet` is available
- `-b`, `--bucket` to chose the bucket from which to take the data
- `-t`, `--token-json-path` to provide token json file path
- `-s`, `--start_date` the last date of the dates period in `ddmmyyyy` format
- `-r`, `--date_range` number of days to take into power users calculation. For example, if start date is 12122022 and range 30 then dates will be since 13-11-2022 to 12-12-2022 inclusively
- `-c`, `--target_smart_contract` smart contract ot analyze. It should be NFT contract


Available options