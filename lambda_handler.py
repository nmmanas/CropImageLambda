import json
import logging
import boto3
from PIL import Image
import io
import os

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

target_bucket = os.environ['TARGET_BUCKET_NAME']


def lambda_handler(event, context):
    logger.info("Lambda function started")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        # Download the image from S3
        logger.info(
            f"Downloading image from bucket: {bucket_name}, key: {object_key}")
        image_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        image_data = image_object['Body'].read()

        # Open the image using Pillow
        with Image.open(io.BytesIO(image_data)) as img:
            # Define the crop box (left, upper, right, lower)
            crop_box = (0, 0, 1080, 1080)
            cropped_img = img.crop(crop_box)

            # Save the cropped image to a bytes buffer
            buffer = io.BytesIO()
            cropped_img.save(buffer, format="JPEG")
            buffer.seek(0)

            # Upload the cropped image back to S3
            cropped_object_key = f"cropped-{object_key}"
            s3_client.put_object(Bucket=target_bucket,
                                 Key=cropped_object_key,
                                 Body=buffer,
                                 ContentType='image/jpeg')
            logger.info(
                f"Successfully cropped and uploaded {cropped_object_key} to {target_bucket}"
            )

        return {
            'statusCode':
            200,
            'body':
            f'Successfully cropped and uploaded {cropped_object_key} to {bucket_name}'
        }
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing image: {str(e)}")
        }
