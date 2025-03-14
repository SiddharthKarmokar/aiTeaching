from src.aiteacher.constants import *
from src.aiteacher.utils.common import read_yaml, create_directories
from src.aiteacher.entity import *

class ConfigurationManager:
    def __init__(self, config_path=CONFIG_FILE_PATH,
                 params_path=PARAMS_FILE_PATH):
        self.config=read_yaml(config_path)
        self.params=read_yaml(params_path)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            contests_dir=config.contests_dir,
            authors_file=config.authors_file
        )
        return data_ingestion_config