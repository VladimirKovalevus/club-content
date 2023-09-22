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

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI(
    title = 'Gateway'
)

class xUser(BaseModel):
    login: str
    password: str
    workspace_name: str

class xFolder(BaseModel):
    path: str
    skip: int
    take: int

class xToken(BaseModel):
    login: str
    workspace_id: str
    exp: int

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return OrderedDict(payload)
    except jwt.ExpiredSignatureError:
        return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# @app.post('/token', response_model=Token,  tags=['Authorization'])
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     # if not user:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail='Incorrect username or password',
#     #         headers={'Authorization': 'Bearer'},
#     #     )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={'sub': user.username}, expires_delta=access_token_expires
#     )
#     return {'access_token': access_token, 'token_type': 'Bearer'}

@app.post('/create_users', tags=['Users'])
async def read_users(person: xUser):
    login = person.login
    password = person.password

    result = grpc_module.CreateWorkspace(person.workspace_name)
    workspace_id = result['workspace_id']

    result = grpc_module.CreateUser(login, password, workspace_id)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': {'login': login, 'workspace_id': workspace_id},}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.get('/create_workspace', tags=['Workspace']) # + workspace_id
async def read_users(name: str):
    result = grpc_module.CreateWorkspace(name)
    return {'data': result['workspace_id']}



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






@app.post('/test/create_users', tags=['Test'])
async def test_create_users(person: xUser):
    login = person.login
    password = person.password

    workspace_id = '123'
    # result = grpc_module.CreateWorkspace(person.workspace_name)
    # workspace_id = result['workspace_id']

    # result = grpc_module.CreateUser(login, password, workspace_id)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': {'login': login, 'workspace_id': workspace_id},}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}

@app.get('/test/create_workspace/{name}', tags=['Test']) # + workspace_id
async def test_create_workspace(name: str, current_user: xToken = Depends(oauth2_scheme)):
    token = decode_jwt(current_user)
    # result = grpc_module.CreateWorkspace(name)
    # return {'data': result['workspace_id']}
    return {'data': token.get('login')}




