from src.aiteacher import logger
from src.aiteacher.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f"Stage: {STAGE_NAME} Initiated")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f"Stage: {STAGE_NAME} Completed")
except Exception as e:
    logger.exception(e)
    raise e