import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGODB_URL")

ca = certifi.where()  # Certificate Authority


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # to load and convert csv to json
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # To insert the data into mongodb
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


# Execution
if __name__ == "__main__":
    FILE_PATH = "Network_data\phisingData.csv"
    DATABASE = "Sidnaik04"
    collection = "NetworkData"

    networkObj = NetworkDataExtract()

    records = networkObj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)

    no_of_records = networkObj.insert_data_mongodb(records, DATABASE, collection)
    print(no_of_records)
