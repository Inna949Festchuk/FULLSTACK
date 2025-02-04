import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from models import Token, ORM_OBJECT, ORM_CLS, User, Token, Role, Right
from fastapi import HTTPException
from sqlalchemy import select, func
from config import DEFAULT_ROLE


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_password(db_password: str, user_password: str) -> bool:
    db_password = db_password.encode()
    user_password = user_password.encode()
    return bcrypt.checkpw(user_password, db_password)


async def get_default_role(session: AsyncSession) -> Role:
    query = select(Role).where(Role.name == DEFAULT_ROLE)
    role = await session.scalar(query)
    return role


async def check_access_rights(
        session: AsyncSession,
        token: Token,
        model: ORM_OBJECT | ORM_CLS,
        write: bool,
        read: bool,
        owner_field: str = "user_id",
        raise_exception: bool = True,
) -> bool:
    # user = token.user
    # for role in user.roles:
    #     for right in role.rights:
    #         if right.write == write and right.read == read and right.model == model._model:
    #             if not right.only_own:
    #                 return True
    #             else:
    #                 if hasattr(model, owner_field) and getattr(model, owner_field) == user.id:
    #                     return True
    # if raise_exception:
    #     raise HTTPException(403, "Access denied")
    # return False
    where_args = []
    where_args.append(
        User.id == Token.user_id
    )
    where_args.append(
        Right.model == model._model
    )
    if write:
        where_args.append(
            Right.write == True
        )
    if read:
        where_args.append(
            Right.read == True
        )

    if hasattr(model, owner_field) and getattr(model, owner_field) != token.user.id:
        where_args.append(
            Right.only_own == False
        )
    right_query = (
        select(func.count(User.id)).join(Role, User.roles).join(Right, Role.rights).
        where(*where_args)
    )
    rights_count = await session.scalar(right_query)
    if rights_count == 0 and raise_exception:
        raise HTTPException(403, "Access denied")
    return rights_count > 0

