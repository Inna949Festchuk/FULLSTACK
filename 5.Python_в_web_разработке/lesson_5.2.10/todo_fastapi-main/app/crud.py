from typing import Any, Dict, List, NamedTuple, Optional

from constants import UNIQUE_VIOLATION
from fastapi import HTTPException
from models import MODEL, MODEL_CLS, Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError


class Items(NamedTuple):
    items: list[MODEL]
    total: int
    page: int


async def get_item(session: Session, model_cls: MODEL_CLS, item_id: int):
    model = await session.get(model_cls, item_id)
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"{model_cls.__name__} not found",
        )
    return model


async def get_items(session: Session, model_cls: MODEL_CLS, ids: List[int]) -> list[MODEL]:
    query = select(model_cls).where(model_cls.id.in_(ids))
    items = (await session.scalars(query)).all()
    return items


async def get_paginated_items(
    session: Session,
    model_cls: MODEL_CLS,
    where_params: Optional[Dict[str, Any]] = None,
    page: int = 1,
    limit: int = 20,
) -> Items:
    query = select(model_cls)
    total_query = select(func.count(model_cls.id))
    where_params = where_params or {}
    where_params_list = [getattr(model_cls, key) == value for key, value in where_params.items()]
    query = query.where(*where_params_list)
    total_query = total_query.where(*where_params_list)

    skip = (page - 1) * limit
    items = (await session.scalars(query.offset(skip).limit(limit))).unique().all()
    total = (await session.scalars(total_query)).first()
    return Items(items=items, total=total, page=page)


async def add_item(session: Session, item: MODEL, commit: bool = True):
    session.add(item)
    if commit:
        try:
            await session.commit()
        except IntegrityError as err:
            await session.rollback()
            if err.orig.pgcode == UNIQUE_VIOLATION:
                raise HTTPException(
                    status_code=409,
                    detail=f"{item.__class__.__name__} already exists",
                )
            else:
                raise err

    return item
