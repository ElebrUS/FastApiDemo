from db.connect import Base, get_session
from functions import CustomFail, verify_password
from schemas.models import (GetAllUserModel, SearchModel, UserModel,
                            UserUpdatePassword)
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.future import select


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    register_date = Column(DateTime)


async def create_user(session: get_session, data: UserModel) -> User:
    user = User(
        username=data.username,
        email=data.email,
        password=data.password,
        register_date=data.register_date
    )
    session.add(user)
    await session.commit()

    return user


async def change_password(session: get_session,
                          data: UserUpdatePassword) -> User:
    stmt = select(User).where(Users.id == data.user_id)
    result = await session.execute(stmt)

    user = result.scalar()
    if user:
        if await verify_password(
                stored_password=user.password,
                provided_password=data.old_password):
            user.password = data.new_password
            await session.commit()

            return user
        else:
            raise CustomFail('Введеный неверный старый пароль')
    else:
        raise CustomFail('Пользователь не найден')


async def delete_user(session: get_session, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)

    user = result.scalar()
    if user:
        await session.delete(user)
        await session.commit()

        return user
    else:
        raise CustomFail('Пользователь не найден')


async def get_users(session: get_session, data: GetAllUserModel) -> [User]:
    stmt = select(User).offset(data.start).limit(data.count)
    result = await session.execute(stmt)
    return result.scalars().all()


async def search_user(session: get_session, data: SearchModel) -> [User]:
    users = []
    db_users = await session.execute(select(User))

    for user in db_users.scalars():
        if data.field == 'username':
            if data.search_text.lower() in user.username.lower():
                users.append(user)
        elif data.field == 'email':
            if data.search_text.lower() in user.email.lower():
                users.append(user)
        elif data.field == 'user_id':
            if data.search_text.lower() in user.user_id.lower():
                users.append(user)
    return users
