import getopt
import sys
import datetime
from user_similarity_near import similarity
from user_similarity_near import config as c
from user_similarity_near import events_data_connectors as dc
import pandas as pd
import csv


if __name__ == '__main__':
    argv = sys.argv[1:]
    options = "ln:b:s:r:c:"
    long_options = ["user_list_source", "local", "network=", "bucket=", "start_date=", "date_range=", "target_smart_contract="]

    entities = list()
    start_date = datetime.date.today() - datetime.timedelta(days=1)
    dates_range = 1
    target_smart_contract = None
    run_local = False
    source = "csv"

    try:
        opts, args = getopt.getopt(argv, options, long_options)

        for opt, value in opts:

            if opt in ("--user_list_source"):
                if (value in ("csv", "google-storage")):
                    source = value
                else:
                    raise ValueError("Wrong value of source. Possible: csv, txt")

            elif opt in ("-l", "--local"):
                run_local = True

            elif opt in ("-n", "--network"):
                network = value

            elif opt in ("-b", "--bucket"):
                bucket_name = value

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

            elif opt in ("-c", "--target_smart_contract"):
                target_smart_contract = value

    except getopt.GetoptError as e:
        print('Error while parsing command line arguments : ' + str(e))

    dates = [start_date - datetime.timedelta(days=x) for x in range(dates_range)]
    print(dates)
    gcs_connector = dc.MetronomoTXCloudStorageConnector(dates, run_local=run_local)
#     data = gcs_connector.getData()
#     data.to_csv("C:/Users/yaroslav/Documents/JupyterNotebooks/df3_near_sparse.csv")
    #remove
    data = pd.read_csv("C:/Users/yaroslav/Documents/JupyterNotebooks/df3_near_sparse.csv")
    if ('Unnamed: 0' in data.columns):
        data = data.drop('Unnamed: 0', axis=1)
    #
    print(sys.getsizeof(data)/1024/1024/1024)

    removeContracts = c.removeContracts
    removeWalletsPercentile = c.removeWalletsPercentile
    removeContractsPercentile = c.removeContractsPercentile
    row, col, similarity = similarity.calculateSimilarity(data, removeWalletsPercentile, removeContractsPercentile, removeContracts)

    with open('similarity.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(row, col, similarity))

    print(len(row))
    print(row)
    print(len(col))
    print(col)
    print(len(similarity))