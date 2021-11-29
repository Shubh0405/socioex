import csv
import boto3
from variables import CONFIG

photo = "image.jpg"

client = boto3.client('rekognition',
                    region_name='ap-south-1',
                    aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                    aws_secret_access_key=CONFIG["AWS_SECRET_KEY"])

async def get_recognition(image):
    with open(image, 'rb') as source_image:
        source_bytes = source_image.read()

    response = client.detect_labels(Image = {'Bytes': source_bytes}, MaxLabels = 5, MinConfidence = 95)
    return response

