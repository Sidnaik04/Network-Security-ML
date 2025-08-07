import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")


# Configuration of Data Ingestion config
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Read data from mongodb and convert to dataframe
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Store data in feature store
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            NetworkSecurityException(e, sys)

    # Perform Train Test Split
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed Train Test Split on dataframe")

            logging.info(
                "Exited split_data_as_train_test method of DataIngestion Class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting Train and Test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info("Exported Train and Test file path")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Initiate data ingestion
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()  # step 1
            dataframe = self.export_data_into_feature_store(dataframe)  # step 2
            self.split_data_as_train_test(dataframe)  # step 3

            dataingestionartifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
