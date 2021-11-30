import boto3
from variables import CONFIG
from PIL import Image
import requests
from io import BytesIO

photo = "image.jpg"

reko_client = boto3.client('rekognition',
                    region_name='ap-south-1',
                    aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                    aws_secret_access_key=CONFIG["AWS_SECRET_KEY"])

def get_image_recognition(image):
    with open(image, 'rb') as source_image:
        source_bytes = source_image.read()

    response = reko_client.detect_labels(Image = {'Bytes': source_bytes}, MaxLabels = 5, MinConfidence = 95)
    return response

def get_image_url_recognition(url):
    response = requests.get(url)
    img = BytesIO(response.content).read()

    response = reko_client.detect_labels(Image = {'Bytes': img}, MaxLabels = 5, MinConfidence = 95)
    return response

