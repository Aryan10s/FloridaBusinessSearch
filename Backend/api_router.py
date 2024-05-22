from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import main

origins = ["*"]

description="""Florida Secretary of State Business Search."""

app = FastAPI(
    title="Florida State Business Crawler",
    description=description,
    summary="Florida Secretary of State Business Search." ,
    version="1.1.0",
)


app.add_middleware(SessionMiddleware, secret_key="4385ec52fe48826a04d34846ccd6d7f2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)