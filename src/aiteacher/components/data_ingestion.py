import os
import urllib.request as request
import zipfile
from src.aiteacher import logger
import subprocess
import pandas as pd
import bz2
from src.aiteacher.entity import *
from src.aiteacher.utils.common import create_directories

class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        if not os.path.exists(self.config.unzip_dir):
            create_directories([self.config.unzip_dir])
            logger.info(f"Cloning dataset from {self.config.source_url}")
            subprocess.run(["git", "clone", self.config.source_url, self.config.unzip_dir], check=True)
            logger.info("Dataset sucessfully cloned.")
        else:
            logger.info(f"Dataset already exists at {self.config.unzip_dir}")

    def decompress_bz2(self, file_path, output_path):
        """Decompress a .bz2 file to a CSV file."""
        with bz2.BZ2File(file_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                f_out.write(f_in.read())

    def extract_data(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                contests_path = self.config.contests_dir
                file_paths = [f for f in os.listdir(contests_path) if f.endswith(".csv.bz2")]

                all_contests = []
                temp_dir = os.path.join(contests_path, "temp_extracted")
                os.makedirs(temp_dir, exist_ok=True)

                for file in file_paths:
                    contest_id = file.split(".")[0]
                    compressed_file_path = os.path.join(contests_path, file)
                    extracted_file_path = os.path.join(temp_dir, f"{contest_id}.csv")
                    
                    self.decompress_bz2(compressed_file_path, extracted_file_path)
                    
                    df = pd.read_csv(extracted_file_path, engine="python", on_bad_lines="skip")
                    df["contest_id"] = contest_id
                    all_contests.append(df)
                    logger.info(f"Loaded {len(df)} records from contest {contest_id}")

                if all_contests:
                    save_path = self.config.local_data_file
                    create_directories([os.path.dirname(save_path)])
                    final_df = pd.concat(all_contests, ignore_index=True)
                    final_df.to_csv(save_path, index=False)
                    logger.info(f"All contests saved to {save_path}.")
                    return save_path
            except Exception as e:
                logger.error(f"Error extracting data: {e}")
                raise
        else:
            logger.info("Extracted files aleardy exists")