from bcrypt import checkpw, gensalt, hashpw
from config import DEFAULT_ROLE
from fastapi import HTTPException
from models import MODEL, MODEL_CLS, Right, Role, Token, User
from sqlalchemy import func, select


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


async def check_access_rights(
    session,
    token: Token,
    model: MODEL | MODEL_CLS,
    write: bool,
    read: bool,
    owner_field="user_id",
    raise_exception=True,
) -> bool:
    """
    Проверяет права владельца токена на модель
    Мы будем джойнить таблицу пользователей с таблицей ролей, а затем с таблицей прав
    В where_args мы будут заданы улсовия:
     - id пользователя равен id пользователя в токене
     - модель права равна имени модели
     - если write=True, то право на запись
     - если read=True, то право на чтение
     - если у модели есть поле владельца, то проверяем, что id владельца равен id пользователя в токене
     - если влоделец не равен id пользователя в токене, то проверяем, что право не только для владельца
    если хотя бы одно право найдено, то возвращаем True
    """

    where_args = [User.id == token.user_id, Right.model == model._model]
    if write:
        where_args.append(Right.write == True)  # noqa: E712
    if read:
        where_args.append(Right.read == True)  # noqa: E712
    if hasattr(model, owner_field) and getattr(model, owner_field) != token.user_id:
        where_args.append(Right.only_own == False)  # noqa: E712
    rights_query = (
        select(func.count(User.id))
        .join(Role, User.roles)
        .join(Right, Role.rights)
        .where(
            *where_args,
        )
    )
    rights_count = (await session.scalars(rights_query)).first()
    if not rights_count and raise_exception:
        raise HTTPException(status_code=403, detail="Access denied")
    return rights_count > 0


async def get_default_role(session) -> Role:
    """
    Возвращает роль по умолчанию
    """
    return (await session.scalars(select(Role).where(Role.name == DEFAULT_ROLE))).first()
