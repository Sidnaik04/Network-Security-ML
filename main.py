import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_validation import DataValidationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_transformation import DataTransformationConfig
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.model_trainer import ModelTrainerConfig

if __name__ == "__main__":
    try:
        # data ingestion
        trainingpipelineconfig = TrainingPipelineConfig()

        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data Initiation is completed")

        # Data validaion
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation is completed")

        # data transformation
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Initiate data transformation")
        data_transformation = DataTransformation(
            data_validation_artifact, data_transformation_config
        )
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        print(data_transformation_artifact)
        logging.info("Data transformation is completed")

        # model training
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        logging.info("Initiate Model training")
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
