import json, boto3
from bson import json_util, ObjectId, binary
from fastapi import Query, APIRouter, Response, status, Request, Header, HTTPException, Depends
from uuid import UUID
from core.connections import export_db_class


twitter_router = APIRouter() 
database = export_db_class()

translate = boto3.client('translate')

# json_util.DEFAULT_JSON_OPTIONS.datetime_representation = 2

# async def verify_authentication(is_authenticated: bool = Header(None, convert_underscores=False)):
#     if not is_authenticated:
#         raise HTTPException(status_code=401, detail="Authentication Required")
#     return is_authenticated

####################### Newsletter APIs #######################

@twitter_router.get('/get-user-data')
async def get_user_data(request:Request, user: str = Query(None)):
    my_collection = database['user_twitter']

    data = list(my_collection.find({"user": user}))

    for d in data:
        t_text = translate.translate_text(Text=d["content"], SourceLanguageCode=d["language"], TargetLanguageCode="en")
        d["content"] = t_text["TranslatedText"] 

    data = json_util.dumps(data)

    return Response(content = data, media_type="application/json", status_code= status.HTTP_200_OK)

    