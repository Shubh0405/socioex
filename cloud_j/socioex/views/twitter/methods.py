import boto3
from bson import json_util
from fastapi import Query, APIRouter, Response, status, Request
from core.connections import export_db_class
from core.fetch_twitter import get_tweets
from core.aws_recognition import get_image_url_recognition
from core.aws_comprehend import get_comp_entities
from core.ibm_tone import get_tone_analysis
from variables import CONFIG

twitter_router = APIRouter() 
database = export_db_class()

translate = boto3.client('translate', 
                        region_name='ap-south-1',
                        aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                        aws_secret_access_key=CONFIG["AWS_SECRET_KEY"])


@twitter_router.get('/get-user-tweets')
async def get_user_tweets(request:Request, user: str = Query(None)):
    my_collection = database['user_tweets']

    data = get_tweets(user)

    for d in data:
        d["user"] = user
        d["text"] = translate.translate_text(Text=d["text"], SourceLanguageCode="auto", TargetLanguageCode="en")["TranslatedText"]
        ex = my_collection.find(d).count()
        if not ex:
            my_collection.insert_one(d)

    data = list(my_collection.find({"user": user}))
    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)


@twitter_router.get('/get-user-data')
async def get_user_data(request:Request, user: str = Query(None)):
    my_collection = database['user_tweets']
    data = list(my_collection.find({"user": user}))

    for d in data:
        if d["image"]:
            d["image_labels"] = get_image_url_recognition(d["image"])["Labels"]
        # d["text_entities"] = get_comp_entities(d["text"])["Entities"]
        d["tweet_tone"] = get_tone_analysis(d["text"])
        
    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)


@twitter_router.get('/get-user-tone')
async def get_user_data(request:Request, user: str = Query(None)):
    my_collection = database['user_tweets']
    data = list(my_collection.find({"user": user}))

    tones = {
      'HAPPY': 0,
      'SAD': 0,
      'EXCITED': 0,
      'NERVOUS': 0,
      'DEPRESSED': 0,
      'ANGER': 0,
      'FEAR': 0,
      'JOY': 0
    }

    for d in data:
        
        x = get_tone_analysis(d["text"])
        tones[x["tone"]] += x["percent"]

    arr = [['Emotion','Percentage']]

    for i in tones:
        arr.append([i,tones[i]])
        
    data = json_util.dumps({"arr":arr})

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)

@twitter_router.get('/get-user-images')
async def get_user_data(request:Request, user: str = Query(None)):
    my_collection = database['user_tweets']
    data = list(my_collection.find({"user": user}))

    for d in data:
        if d["image"]:
            d["image_labels"] = get_image_url_recognition(d["image"])["Labels"]
        
    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)


@twitter_router.get('/get-test-response')
async def get_user_data(request:Request):
    data = {
        "test": "response",
        "test2": "data"
    }
    data = json_util.dumps(data)
    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)
