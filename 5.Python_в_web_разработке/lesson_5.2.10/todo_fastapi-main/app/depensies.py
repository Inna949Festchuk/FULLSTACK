import datetime
import uuid
from typing import Annotated, AsyncGenerator

from config import TOKEN_TTL
from fastapi import Depends, Header, HTTPException
from models import Session, Token
from sqlalchemy import select


async def get_db_session() -> AsyncGenerator[Session, None]:
    async with Session() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_db_session, use_cache=True)]


async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency) -> Token:
    token_query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=TOKEN_TTL),
    )
    token = (await session.scalars(token_query)).first()
    if token:
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


TokenDependency = Annotated[Token, Depends(get_token)]
