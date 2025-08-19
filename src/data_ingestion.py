import os
import kagglehub
import shutil
from src.logger import get_logger
from src.custom_exception import CustomException
from config.data_ingestion_config import *
import zipfile

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self,dataset_name:str , target_dir:str):
        self.dataset_name = dataset_name
        self.target_dir = target_dir

    def create_raw_dir(self):
        raw_dir = os.path.join(self.target_dir,"raw")  
        if not os.path.exists(raw_dir):
            try:
                os.makedirs(raw_dir)
                logger.info(f"Created the {raw_dir}")
            except Exception as e:
                logger.error("Erro while creating directory..")
                raise CustomException("Faile to create raw dir" , e)
        return raw_dir

    def extract_images_and_labels(self, path: str, raw_dir: str):
        try:
            if path.endswith('.zip'):
                logger.info("Extracting zip file")
                
                extract_dir = os.path.join(raw_dir, "extracted")
                os.makedirs(extract_dir, exist_ok=True)
                
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                logger.info(f"File after extraction: {os.listdir(extract_dir)}")

            # The extracted folder might have a top-level folder like "Guns-Dataset-master"
            extracted_subfolder = os.path.join(extract_dir, os.listdir(extract_dir)[0])
            images_folder = os.path.join(extracted_subfolder, "Images")
            labels_folder = os.path.join(extracted_subfolder, "Labels")

            if os.path.exists(images_folder):
                shutil.move(images_folder, os.path.join(raw_dir, "Images"))
                logger.info("Images moved successfully.")
            else:
                logger.info("Images folder doesn't exist.")

            if os.path.exists(labels_folder):
                shutil.move(labels_folder, os.path.join(raw_dir, "Labels"))
                logger.info("Labels moved successfully.")
            else:
                logger.info("Labels folder doesn't exist.")

        except Exception as e:
            logger.error("Error while extracting.")
            raise CustomException("Error while extracting..", e)

    def download_datset(self, raw_dir: str):
        try:
            import requests
            import os

            # Use the GitHub URL here
            zip_path = os.path.join(raw_dir, "dataset.zip")

            response = requests.get(GITHUB_URL)  # <-- use GITHUB_URL
            response.raise_for_status()
            with open(zip_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded dataset from {GITHUB_URL}")
            self.extract_images_and_labels(zip_path, raw_dir)

        except Exception as e:
            logger.error("Error while downloading data")
            raise CustomException("Error while downloading data", e)


        
    def run(self):
        try:
            raw_dir = self.create_raw_dir()
            self.download_datset(raw_dir)

        except Exception as e:
                logger.error("Error while data ingestion pipeline")
                raise CustomException("Erro while data ingestion pipeline" , e)
        
if __name__=="__main__":
     data_ingestion = DataIngestion(DATASET_NAME,TARGET_DIR)
     data_ingestion.run()

        


                