import json
import os
from typing import Optional
import pandas as pd
import requests
from raga.validators.dataset_validations import DatasetValidator
from raga.utils.http_client import HTTPClient
from raga.dataset_creds import DatasetCreds
from raga.utils.raga_config_reader import read_raga_config, get_config_value
import logging
import zipfile

logger = logging.getLogger(__name__)
config_data = read_raga_config(".raga")


class FileUploadError(Exception):
    pass


class Dataset:
    def __init__(
        self,
        token: str,
        experiment_id: int,
        test_df: pd.DataFrame,
        test_schema,
        name: str,
        creds: Optional[DatasetCreds] = None,
    ):
        self.token = DatasetValidator.validate_token(token)
        self.experiment_id = DatasetValidator.validate_experiment_id(experiment_id)
        self.test_df = DatasetValidator.validate_test_df(test_df)
        self.test_schema = test_schema
        self.name = DatasetValidator.validate_name(name)
        self.creds = DatasetValidator.validate_creds(creds)
        self.csv_file = f"experiment_{self.experiment_id}.csv"
        self.zip_file = f"experiment_{self.experiment_id}.zip"
        self.http_client = HTTPClient(get_config_value(config_data, "default", "api_host"))
        self.load_data_frame()

    def load_data_frame(self):
        """
        Loads the data frame, creates a CSV file, zips it, and uploads it to the server.
        """
        logger.debug("Loading Data Frames")
        self.create_csv_and_zip_from_data_frame()
        pre_signed_url = self.get_pre_signed_s3_url(self.zip_file)
        self.upload_file(
            pre_signed_url,
            self.zip_file,
            success_callback=self.on_upload_success,
            failure_callback=self.on_upload_failed,
        )
        self.delete_files()
        self.notify_server()

    def load_labels_from_file(
        self,
        path_to_file,
        format,
        image_id,
        type,
        label_name,
        col_name,
        class_map,
    ):
        """
        Loads labels from a file, zips it, and uploads it to the server.

        Args:
            path_to_file (str): The path to the file containing labels.
            format (str): The format of the labels.
            image_id (str): The ID of the image.
            type (str): The type of the labels.
            label_name (str): The name of the label.
            col_name (str): The name of the column.
            class_map (dict): The class map.

        Raises:
            ValueError: If any required parameter is missing.
        """
        required_params = [
            "format",
            "image_id",
            "type",
            "label_name",
            "col_name",
            "class_map",
        ]
        for param in required_params:
            if not locals().get(param):
                raise ValueError(f"{param.capitalize().replace('_', ' ')} is required.")
        file_dir = os.path.dirname(path_to_file)
        file_name_without_ext, file_extension, file_name = self.get_file_name(path_to_file)
        zip_file_name = os.path.join(file_dir, file_name_without_ext + ".zip")
        with zipfile.ZipFile(zip_file_name, "w") as zip_file:
            zip_file.write(path_to_file, file_name)
        pre_signed_url = self.get_pre_signed_s3_url(file_name_without_ext + ".zip")
        self.upload_file(
            pre_signed_url,
            zip_file_name,
            success_callback=self.on_upload_success,
            failure_callback=self.on_upload_failed,
        )
        if os.path.exists(zip_file_name):
            os.remove(zip_file_name)
            logger.debug("Zip file deleted")
        else:
            logger.debug("Zip file not found")

        self.notify_server()

    def get_pre_signed_s3_url(self, file_name):
        """
        Generates a pre-signed URL for uploading the file to an S3 bucket.

        Args:
            file_name (str): The name of the file.

        Returns:
            str: The pre-signed S3 URL.

        Raises:
            ValueError: If the file name is missing.
        """
        res_data = self.http_client.post(
            "api/experiment/uploadPath",
            {"experimentId": self.experiment_id, "fileName": file_name},
            {"Authorization": f'Bearer {self.token}'},
        )
        logger.debug("Pre-signed URL generated")
        return res_data["data"]["uploadPath"]

    def upload_file(self, pre_signed_url, file_path, success_callback=None, failure_callback=None):
        """
        Uploads a file to the server using a pre-signed URL.

        Args:
            pre_signed_url (str): The pre-signed URL for uploading the file.
            file_path (str): The path of the file to be uploaded.
            success_callback (Optional[function]): The callback function to be called on successful upload.
            failure_callback (Optional[function]): The callback function to be called on upload failure.

        Raises:
            ValueError: If the pre-signed URL or file path is missing.
            FileUploadError: If there is an error uploading the file.
        """
        if not pre_signed_url:
            raise ValueError("Pre-signed URL is required.")
        if not file_path:
            raise ValueError("File path is required.")
        logger.debug(f"UPLOADING {file_path}")
        try:
            with open(file_path, "rb") as file:
                response = requests.put(pre_signed_url, data=file)
                response.raise_for_status()  # Raise an exception for HTTP errors
                if response.status_code == 200:
                    if success_callback:
                        success_callback()
                    return True
                else:
                    if failure_callback:
                        failure_callback(response.status_code)
                    raise FileUploadError(f"File upload failed with status code: {response.status_code}")
        except requests.RequestException as e:
            if failure_callback:
                failure_callback(str(e))
            raise FileUploadError(f"Error uploading file: {e}")

    def notify_server(self):
        """
        Notifies the server to load the dataset with the provided experiment ID and data definition.
        """
        res_data = self.http_client.post(
            "api/experiment/pushToEs",
            {"experimentId": self.experiment_id, "dataDefinition": self.test_schema.__dict__},
            {"Authorization": f'Bearer {self.token}'},
        )
        logger.debug("Notified the server to load the dataset")

    def create_csv_and_zip_from_data_frame(self):
        """
        Creates a CSV file from the data frame and compresses it into a zip file.
        """
        # Validate the CSV file path
        if not self.csv_file or not isinstance(self.csv_file, str):
            raise ValueError("Invalid CSV file path. Please provide a valid file path.")

        # Save the DataFrame as a CSV file
        self.test_df.to_csv(self.csv_file, index=False)
        logger.debug("Data frame has been saved to CSV")

        # Create a zip file containing the CSV file
        with zipfile.ZipFile(self.zip_file, "w") as zip_file:
            zip_file.write(self.csv_file, os.path.basename(self.csv_file))

        logger.debug(f"CSV file has been zipped: {self.zip_file}")

    def get_file_name(self, file_path):
        """
        Extracts the file name, extension, and file name without extension from the given file path.

        Args:
            file_path (str): The path of the file.

        Returns:
            Tuple[str, str, str]: The file name without extension, file extension, and file name.

        Raises:
            ValueError: If the file path is invalid.
        """
        if not isinstance(file_path, str):
            raise ValueError("Invalid file path. Please provide a valid file path string.")

        file_name = os.path.basename(file_path)
        file_name_without_ext, file_extension = os.path.splitext(file_name)

        if file_extension:
            return file_name_without_ext, file_extension, file_name
        else:
            return file_name_without_ext, "", file_name
        

    def delete_files(self):
        """
        Deletes the CSV and zip files associated with the dataset.
        """
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
            logger.debug("CSV file deleted")
        else:
            logger.debug("CSV file not found")

        if os.path.exists(self.zip_file):
            os.remove(self.zip_file)
            logger.debug("Zip file deleted")
        else:
            logger.debug("Zip file not found")
            

    def on_upload_success(self):
        """
        Callback function to be called on successful file upload.
        """
        logger.debug("File uploaded successfully")

    def on_upload_failed(self):
        """
        Callback function to be called on file upload failure.
        """
        logger.debug("File upload failed")
