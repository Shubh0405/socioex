import boto3
from variables import CONFIG

comp_client = boto3.client('comprehend',
                            region_name='ap-south-1',
                            aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                            aws_secret_access_key=CONFIG["AWS_SECRET_KEY"])


def get_comp_entities(cap):
    sentiment_output = comp_client.detect_entities(Text=cap, LanguageCode='en')
    return sentiment_output