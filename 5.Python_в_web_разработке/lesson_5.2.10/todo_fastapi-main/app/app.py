import datetime

import fastapi
import schema
from auth import check_access_rights, check_password, get_default_role, hash_password
from crud import add_item, get_item, get_items, get_paginated_items
from depensies import SessionDependency, TokenDependency
from fastapi import Depends
from models import Right, Role, Todo, Token, User
from sqlalchemy import select

app = fastapi.FastAPI(
    title="Todo API",
    version="1.0",
    description="A simple TODO API",
)


@app.post("/v1/login/", response_model=schema.Token, tags=["token"], summary="Login")
async def login(user: schema.Login, session: SessionDependency) -> Token:
    user_query = select(User).where(User.name == user.name).execution_options()
    user_model = (await session.scalars(user_query)).first()
    if user_model and check_password(user.password, user_model.password):
        token = Token(user_id=user_model.id)
        session.add(token)
        await session.commit()
        return schema.Token(token=token.token)
    raise fastapi.HTTPException(
        status_code=401,
        detail="Invalid username or password",
    )


@app.post(
    "/v1/user/",
    response_model=schema.CreateUserResponse,
    tags=["user"],
    summary="Register user",
)
async def create_user(
    user: schema.Register,
    session: SessionDependency,
) -> schema.CreateUserResponse:
    role = await get_default_role(session)
    user = User(
        name=user.name,
        password=hash_password(
            user.password,
        ),
        roles=[role],
    )
    user = await add_item(session, user)
    return schema.CreateUserResponse(
        id=user.id,
        name=user.name,
        registration_time=user.registration_time,
    )


@app.get("/v1/user/{user_id}", response_model=schema.GetUserResponse, tags=["user"], summary="Get user")
async def get_user(user_id: int, token: TokenDependency, session: SessionDependency) -> schema.GetUserResponse:
    user = await get_item(session, User, user_id)
    await check_access_rights(session, token, user, write=False, read=True, owner_field="id")
    return schema.GetUserResponse(
        id=user.id,
        name=user.name,
        registration_time=user.registration_time,
        todos=[todo.id for todo in user.todos],
        roles=[role.id for role in user.roles],
    )


@app.patch("/v1/user/{user_id}", response_model=schema.UpdateUserResponse, tags=["user"], summary="Update user")
async def update_user(
    user_id: int, user: schema.UpdateUser, token: TokenDependency, session: SessionDependency
) -> schema.UpdateUserResponse:
    user_model = await get_item(session, User, user_id)
    await check_access_rights(session, token, user_model, write=True, read=False, owner_field="id")
    for field, value in user.dict(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)
        setattr(user_model, field, value)
    user_model = await add_item(session, user_model)
    return schema.UpdateUserResponse(
        id=user_model.id,
        name=user_model.name,
        registration_time=user_model.registration_time,
        todos=[todo.id for todo in user_model.todos],
        roles=[role.id for role in user_model.roles],
    )


@app.delete("/v1/user/{user_id}", response_model=schema.DeleteUserResponse, tags=["user"], summary="Delete user")
async def delete_user(user_id: int, token: TokenDependency, session: SessionDependency) -> schema.DeleteUserResponse:
    user = await get_item(session, User, user_id)
    await check_access_rights(session, token, user, write=True, read=False, owner_field="id")
    await session.delete(user)
    await session.commit()
    return schema.DeleteUserResponse(status="deleted")


@app.get(
    "/v1/right/{right_id}/",
    response_model=schema.Right,
    tags=["right"],
    summary="Get right",
)
async def get_right(
    right_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Right:
    await check_access_rights(session, token, Right, write=False, read=True)
    right = await get_item(session, Right, right_id)
    return right


@app.get(
    "/v1/right/",
    response_model=schema.PaginatedRightsResponse,
    tags=["right"],
    summary="Get rights",
)
async def get_rights(
    token: TokenDependency,
    session: SessionDependency,
    query_params: schema.PaginatedRightsRequest = Depends(
        schema.PaginatedRightsRequest,
    ),
) -> schema.PaginatedRightsResponse:
    await check_access_rights(session, token, Right, write=False, read=True)
    rights = await get_paginated_items(
        session,
        Right,
        query_params.dict(exclude_none=True, exclude={"page", "limit"}),
        page=query_params.page,
        limit=query_params.limit,
    )
    return schema.PaginatedRightsResponse(
        rights=[schema.Right(**item.dict) for item in rights.items], page=rights.page, total=rights.total
    )


@app.post(
    "/v1/right/",
    response_model=schema.Right,
    tags=["right"],
    summary="Create a right",
)
async def create_right(
    right: schema.CreateRight,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Right:
    await check_access_rights(session, token, Right, write=True, read=False)
    right = Right(**right.dict())
    right = await add_item(session, right)
    return right


@app.patch(
    "/v1/right/{right_id}",
    response_model=schema.Right,
    tags=["right"],
    summary="Update right",
)
async def update_right(
    right_id: int,
    right: schema.UpdateRight,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Right:
    await check_access_rights(session, token, Right, write=True, read=False)
    right_model = await get_item(session, Right, right_id)
    for field, value in right.dict(exclude_unset=True).items():
        setattr(right_model, field, value)
    right_model = await add_item(session, right_model)
    return right_model


@app.delete(
    "/v1/right/{right_id}",
    response_model=schema.DeleteRightResponse,
    tags=["right"],
    summary="Delete right",
)
async def delete_right(
    right_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.DeleteRightResponse:
    await check_access_rights(session, token, Right, write=True, read=False)
    right = await get_item(session, Right, right_id)
    await session.delete(right)
    await session.commit()
    return schema.DeleteRightResponse(status="deleted")


@app.get(
    "/v1/role/",
    response_model=schema.PaginatedRolesResponse,
    tags=["role"],
    summary="Get roles",
)
async def get_roles(
    token: TokenDependency,
    session: SessionDependency,
    query_params: schema.PaginatedRolesRequest = Depends(
        schema.PaginatedRolesRequest,
    ),
) -> schema.PaginatedRolesResponse:
    await check_access_rights(session, token, Role, write=False, read=True)
    roles = await get_paginated_items(
        session,
        Role,
        query_params.dict(exclude_none=True, exclude={"page", "limit"}),
        page=query_params.page,
        limit=query_params.limit,
    )

    return schema.PaginatedRolesResponse(
        roles=[
            schema.Role(id=item.id, name=item.name, rights=[schema.Right(**right.dict) for right in item.rights])
            for item in roles.items
        ],
        page=roles.page,
        total=roles.total,
    )


@app.get(
    "/v1/role/{role_id}",
    response_model=schema.Role,
    tags=["role"],
    summary="Get role",
)
async def get_role(
    role_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Role:
    await check_access_rights(session, token, Role, write=False, read=True)
    role = await get_item(session, Role, role_id)
    return role


@app.post(
    "/v1/role/",
    response_model=schema.CreateRoleResponse,
    tags=["role"],
    summary="Create role",
)
async def create_role(
    role: schema.CreateRole,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.CreateRoleResponse:
    await check_access_rights(session, token, Role, write=True, read=False)
    role = Role(**role.dict())
    role = await add_item(session, role)
    return schema.CreateRoleResponse(
        id=role.id,
        name=role.name,
    )


@app.patch(
    "/v1/role/{role_id}",
    response_model=schema.UpdateRoleResponse,
    tags=["role"],
    summary="Update role",
)
async def update_role(
    role_id: int,
    role: schema.UpdateRole,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.UpdateRoleResponse:
    await check_access_rights(session, token, Role, write=True, read=False)
    role_model = await get_item(session, Role, role_id)

    if role.rights:
        await check_access_rights(session, token, Right, write=False, read=True)
        rights = await get_items(session, Right, role.rights)
        role_model.rights = rights

    for field, value in role.dict(exclude_unset=True, exclude={"rights"}).items():
        setattr(role_model, field, value)

    role_model = await add_item(session, role_model)

    return schema.UpdateRoleResponse(
        id=role_model.id,
        name=role_model.name,
        rights=[right.id for right in role_model.rights],
    )


@app.delete(
    "/v1/role/{role_id}",
    response_model=schema.DeleteRoleResponse,
    tags=["role"],
    summary="Delete role",
)
async def delete_role(
    role_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.DeleteRoleResponse:
    await check_access_rights(session, token, Role, write=True, read=False)
    role = await get_item(session, Role, role_id)
    await session.delete(role)
    await session.commit()
    return schema.DeleteRoleResponse(status="deleted")


@app.get(
    "/v1/todo/",
    response_model=schema.PaginatedTodosResponse,
    tags=["todo"],
    summary="Get todos",
)
async def get_todos(
    token: TokenDependency,
    session: SessionDependency,
    query_params: schema.PaginatedTodosRequest = Depends(
        schema.PaginatedTodosRequest,
    ),
) -> schema.PaginatedTodosResponse:
    params = query_params.dict(exclude_none=True, exclude={"page", "limit"})
    if check_access_rights(session, token, Todo, write=False, read=True, raise_exception=False):
        #  Если пользователь может видеть только свои задачи, то добавляем это условие
        params["user_id"] = token.user_id

    todos = await get_paginated_items(
        session,
        Todo,
        params,
        page=query_params.page,
        limit=query_params.limit,
    )

    return schema.PaginatedTodosResponse(
        todos=[schema.Todo(**item.dict) for item in todos.items], page=todos.page, total=todos.total
    )


@app.get(
    "/v1/todo/{todo_id}",
    response_model=schema.Todo,
    tags=["todo"],
    summary="Get todo",
)
async def get_todo(
    todo_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Todo:
    todo = await get_item(session, Todo, todo_id)
    await check_access_rights(session, token, todo, write=False, read=True, owner_field="user_id")
    return todo


@app.post(
    "/v1/todo/",
    response_model=schema.Todo,
    tags=["todo"],
    summary="Create todo",
)
async def create_todo(
    todo: schema.CreateTodo,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Todo:
    if not todo.user_id:
        todo.user_id = token.user_id
    todo = Todo(**todo.dict())
    await check_access_rights(session, token, todo, write=True, read=False, owner_field="user_id")
    todo = await add_item(session, todo)
    return todo


@app.patch(
    "/v1/todo/{todo_id}",
    response_model=schema.Todo,
    tags=["todo"],
    summary="Update todo",
)
async def update_todo(
    todo_id: int,
    todo: schema.UpdateTodoRequest,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.Todo:
    todo_model = await get_item(session, Todo, todo_id)
    await check_access_rights(session, token, todo_model, write=True, read=False, owner_field="user_id")
    payload = todo.dict(exclude_unset=True)
    if "done" in payload:
        payload["finish_time"] = datetime.datetime.now()
    for field, value in payload.items():
        setattr(todo_model, field, value)
    todo_model = await add_item(session, todo_model)
    return todo_model


@app.delete(
    "/v1/todo/{todo_id}",
    response_model=schema.DeleteTodoResponse,
    tags=["todo"],
    summary="Delete todo",
)
async def delete_todo(
    todo_id: int,
    token: TokenDependency,
    session: SessionDependency,
) -> schema.DeleteTodoResponse:
    todo = await get_item(session, Todo, todo_id)
    await check_access_rights(session, token, todo, write=True, read=False, owner_field="user_id")
    await session.delete(todo)
    await session.commit()
    return schema.DeleteTodoResponse(status="deleted")
