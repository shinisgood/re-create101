import boto3, uuid, io, os
from PIL import Image

from create101.settings    import AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_S3_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME


class S3FileUpload:
    s3 = boto3.resource(
        "s3",
        aws_access_key_id= AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_S3_SECRET_ACCESS_KEY,
    )

    @staticmethod
    def resize_image(**kwargs):
        STANDARD_WIDTH_SIZE = 1024
        STANDARD_HEIGHT_SIZE = 768
        IMAGE_RATIO = 1.33

        resized_images = {}

        for k, v in kwargs.items():
            with Image.open(v) as image:
                width_size = image.size[0]
                height_size = image.size[1]

                if width_size / height_size < IMAGE_RATIO:
                    size = (
                        STANDARD_WIDTH_SIZE,
                        int(image.size[1] * (STANDARD_WIDTH_SIZE / image.size[0])),
                    )
                else:
                    size = (
                        int(image.size[0] * (STANDARD_HEIGHT_SIZE / image.size[1])),
                        STANDARD_HEIGHT_SIZE,
                    )
                print(size)
                resized_image = image.resize(size)
                resized_image = image.convert("RGB")

                byte_array = io.BytesIO()
                resized_image.save(byte_array, format="JPEG")
                byte_array.seek(0)
                resized_images[k] = byte_array

            return resized_images

    @staticmethod
    def generate_filname(**kwargs):
        filename = {}

        for k, v in kwargs.items():
            file_name = str(uuid.uuid1())
            filename[k] = file_name

        return filename

    @classmethod
    def file_upload(cls, filename, **kwargs):

        for k, v in kwargs.items():
            cls.s3.Bucket(AWS_S3_STORAGE_BUCKET_NAME).put_object(
                Key=filename[k], Body=v, ContentType="image/jpeg"
            )
