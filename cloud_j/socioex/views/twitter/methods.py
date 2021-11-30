import boto3
from bson import json_util
from fastapi import Query, APIRouter, Response, status, Request
from core.connections import export_db_class
from core.fetch_twitter import get_tweets
from core.aws_recognition import get_image_recognition, get_image_url_recognition
from variables import CONFIG

twitter_router = APIRouter() 
database = export_db_class()

translate = boto3.client('translate', 
                        region_name='ap-south-1',
                        aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                        aws_secret_access_key=CONFIG["AWS_SECRET_KEY"])


@twitter_router.get('/get-user-data')
async def get_user_data(request:Request, user: str = Query(None)):
    my_collection = database['user_twitter']
    print(database)
    print(my_collection)

    data = list(my_collection.find({"user": user}))
    data2 = list(my_collection.find({}))
    print(len(data2))

    for d in data:
        t_text = translate.translate_text(Text=d["content"], SourceLanguageCode=d["language"], TargetLanguageCode="en")
        d["content"] = t_text["TranslatedText"] 

    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)

@twitter_router.get('/get-user-twitter')
async def get_user_twitter(request:Request, user: str = Query(None)):
    data = get_tweets(user)

    for d in data:
        d["text"] = translate.translate_text(Text=d["text"], SourceLanguageCode="auto", TargetLanguageCode="en")["TranslatedText"]
        if d["image"]:
            d["image_labels"] = get_image_url_recognition(d["image"])

    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)

@twitter_router.get('/get-recognition')
async def get_recognition(request:Request, url: str = Query(None)):
    data = get_image_url_recognition(url)

    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)

    