from src.aiteacher.config.configurations import ConfigurationManager
from src.aiteacher.components.data_ingestion import DataIngestion
from src.aiteacher import logger


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.extract_data()
    
    