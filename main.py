from typing import List

from db.connect import Base, engine, get_session
from db.models import (change_password, create_user, delete_user, get_users,
                       search_user)
from fastapi import Depends, FastAPI, HTTPException
from functions import CustomFail
from schemas.models import (GetAllUserModel, SearchModel, UserInModel,
                            UserModel, UserUpdatePassword)
from sqlalchemy.exc import IntegrityError

app = FastAPI()


async def get_db():
    session = await get_session()
    try:
        yield session
    finally:
        await session.close()


@app.get('/')
async def welcome():
    return {'text': 'Hello World'}


@app.post('/create-user/',
          response_description='Add User',
          response_model=UserModel)
async def add_user(user: UserInModel, session: get_session = Depends(get_db)):
    try:
        return await create_user(session, user)
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' \
           ' "ix_users_email"' in str(e):
            raise HTTPException(status_code=400,
                                detail="Данный Email уже существует")
        elif 'duplicate key value violates unique constraint' \
             ' "ix_users_username"' in str(e):
            raise HTTPException(status_code=400,
                                detail="Данный Username уже существует")


@app.post('/update-password/',
          response_description='Change Password',
          response_model=UserModel)
async def modify_password(user: UserUpdatePassword,
                          session: get_session = Depends(get_db)):
    try:
        return await change_password(session, user)
    except CustomFail as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/delete-user/{user_id}',
          response_description='Delete User',
          response_model=UserModel)
async def del_user(user_id: int, session: get_session = Depends(get_db)):
    try:
        return await delete_user(session, user_id)
    except CustomFail as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/get-user-list/',
          response_description='Get All User',
          response_model=List[UserModel])
async def del_user(all_user: GetAllUserModel,
                   session: get_session = Depends(get_db)):
    return await get_users(session, all_user)


@app.post('/search/',
          response_description='Search User',
          response_model=List[UserModel])
async def search(search_model: SearchModel,
                 session: get_session = Depends(get_db)):
    return await search_user(session, search_model)

