import datetime
import uuid
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from models import Session, Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import TOKEN_TTL


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]


async def get_token(
        x_token: Annotated[uuid.UUID, Header()],
        session: SessionDependency
) -> Token:
    token_query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >=
        datetime.datetime.utcnow() - datetime.timedelta(
            seconds=TOKEN_TTL
        )

    )
    token = await session.scalar(token_query)
    if token is None:
        raise HTTPException(401, "Invalid token")
    return token


TokenDependency = Annotated[AsyncSession, Depends(get_token)]