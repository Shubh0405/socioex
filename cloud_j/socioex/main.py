from fastapi import FastAPI, APIRouter, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from views.twitter.methods import twitter_router

app = FastAPI(docs_url=None, redoc_url=None)


# router = APIRouter()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    twitter_router,
    prefix="/twitter",
    tags = ["Twitter"]
)