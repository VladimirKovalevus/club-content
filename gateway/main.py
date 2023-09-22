from collections import OrderedDict
from typing import List
import logging
from jose import jwt
from typing import Annotated 
from pydantic import BaseModel, Field
from fastapi import FastAPI, status, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta

import grpc_module


SECRET_KEY = 'you_wont_pass_man'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

class xUser(BaseModel):
    login: str
    password: str
    workspace_id: str

class xFolder(BaseModel):
    path: str
    skip: int
    take: int

@app.post('/create_users', tags=['Users'])
async def read_users(person: xUser):
    return {'data': person}

@app.get('/create_workspace', tags=['Workspace'])
async def read_users(name: str):
    return {'data': name}

@app.post('/create_file', tags=['File']) # + workspace_id
async def read_users(path: str, file: UploadFile = File(None)):
    return {'data': str(file.file.read()), 'path': path}

@app.post('/create_folder', tags=['Folder']) # + workspace_id
async def read_users(folder: xFolder):
    return {'data': folder}



logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'), 
        logging.StreamHandler()  
    ]
)

