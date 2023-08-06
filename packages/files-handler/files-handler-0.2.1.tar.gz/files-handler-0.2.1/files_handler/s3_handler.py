# Importing libraries
import boto3
import botocore
import os
import tqdm
from files_handler.folders_handler import folders_handler


class s3_handler:
    """
    Deal with files and connection to S3.

    :param bucket: The Bucket.
    :type bucket: string
    :param path_ref: Reference Path to manage the files and folders.
    :type path_ref: string
    """

    def __init__(self, bucket, path_ref, input_path="input", result_path="output"):
        self.session = boto3.Session()
        self.bucket = bucket
        self.path_ref = path_ref
        self.path_to_predict_images = os.path.join(path_ref, input_path)
        self.s3_client = boto3.client("s3")
        self.folders_handler = folders_handler("")

    # Get image from s3 bucket
    def get_image_from_s3_bucket(
        self,
        s3_image_path,
        local_download_path="",
        progress_bar=True,
        create_folder=True,
        quiet=False,
    ):
        """
        Get an image from S3 passing the image path on s3 and saving on reference path + input

        :param s3_image_path: The s3 path of image with the image name.
        :type s3_image_path: string
        :param local_download_path: Local path to download image, if you desire to use a different path than "input_path"
        :type local_download_path: string
        :param progress_bar: Enable progress bar for download
        :type progress_bar: boolean
        :param create_folder: Enable folder creation for downloaded file
        :type create_folder: boolean
        :param quiet: Disable print of messages along code
        :type quiet: boolean

        :return: If the image was downloaded or not.
        :type: boolean
        """
        try:
            if local_download_path == "":
                download_path = self.path_to_predict_images
            else:
                download_path = local_download_path

            if create_folder:
                self.folders_handler.verify_and_create_folder(
                    download_path, "Creating input directory...", quiet=quiet
                )

            image_name = os.path.basename(s3_image_path)
            local_image_path = os.path.join(download_path, image_name).replace(
                "\\", "/"
            )

            if not quiet:
                print(f"Downloading file: {image_name} to {download_path} folder")
            s3 = self.session.resource("s3")
            bucket = s3.Bucket(self.bucket)

            if progress_bar:
                meta_data = self.s3_client.head_object(
                    Bucket=self.bucket, Key=s3_image_path
                )
                total_length = int(meta_data.get("ContentLength", 0))
                with tqdm.tqdm(
                    total=total_length, unit="B", unit_scale=True, desc=s3_image_path
                ) as pbar:
                    bucket.download_file(
                        s3_image_path,
                        local_image_path,
                        Callback=lambda bytes_transferred: pbar.update(
                            bytes_transferred
                        ),
                    )

            else:
                bucket.download_file(s3_image_path, local_image_path)

            if not quiet:
                print("File Downloaded")
            return True

        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    # Upload resulting image to s3 bucket
    def upload_image_to_s3_bucket(
        self, local_image_path, s3_output_path, progress_bar=True, quiet=False
    ):
        """
        Upload an image to S3 passing the image path on s3 and the S3 Output Path

        :param local_image_path: The path of the image locally with the image name
        :type local_image_path: string
        :param s3_output_path: The path of the image on S3
        :type s3_output_path: string
        :param progress_bar: Enable progress bar for upload
        :type progress_bar: boolean
        :param quiet: Disable print of messages along code
        :type quiet: boolean

        :return: If the image was uploaded or not.
        :rtype: boolean
        """
        try:
            if not quiet:
                print(f"Uploading results to {s3_output_path}")
            s3 = self.session.resource("s3")
            bucket = s3.Bucket(self.bucket)

            image_name = os.path.basename(local_image_path)
            s3_image_path = os.path.join(s3_output_path, image_name).replace("\\", "/")
            if not quiet:
                print(f"Complete path: {s3_image_path}")

            if progress_bar:
                with tqdm.tqdm(
                    total=os.stat(local_image_path).st_size,
                    unit="B",
                    unit_scale=True,
                    desc=image_name,
                ) as pbar:
                    bucket.upload_file(
                        local_image_path,
                        s3_image_path,
                        Callback=lambda bytes_transferred: pbar.update(
                            bytes_transferred
                        ),
                    )

            else:
                bucket.upload_file(local_image_path, s3_image_path)

            return True

        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    def check_if_file_exists(self, file_name, s3_path, quiet=False):
        """
        Check if file exists in s3 bucket

        :param file_name: The name of the file
        :type file_name: string
        :param s3_path: The path of the file on S3
        :type s3_path: string
        :param quiet: Disable print of messages along code
        :type quiet: boolean

        :return: If the file exists or not.
        :rtype: boolean
        """
        try:
            s3 = self.session.resource("s3")
            try:
                s3.Object(
                    self.bucket, os.path.join(s3_path, file_name).replace("\\", "/")
                ).load()
                if not quiet:
                    print("File exists")
                return True
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    # The object does not exist.
                    if not quiet:
                        print("File does not exist")
                    return False
                else:
                    # Something else has gone wrong.
                    raise
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
