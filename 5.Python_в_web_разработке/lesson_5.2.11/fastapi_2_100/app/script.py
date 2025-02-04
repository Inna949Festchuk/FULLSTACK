from models import Role, Right, Session, Todo, User
from sqlalchemy.ext.asyncio import AsyncSession
from config import DEFAULT_ROLE
import asyncio

async def create_default_role(session: AsyncSession):

    right_todo_self_read = Right(
        model=Todo._model,
        only_own=True,
        read=True,
        write=False
    )

    right_todo_self_write = Right(
        model=Todo._model,
        only_own=True,
        read=False,
        write=True
    )

    right_user_self_read = Right(
        model=User._model,
        only_own=True,
        read=True,
        write=False
    )

    right_user_self_write = Right(
        model=User._model,
        only_own=True,
        read=False,
        write=True
    )

    role = Role(name=DEFAULT_ROLE, rights=[right_todo_self_read,
                                           right_todo_self_write,
                                           right_user_self_read,
                                           right_user_self_write
                                           ])
    session.add_all([role, right_todo_self_read,
                     right_todo_self_write,
                     right_user_self_read,
                     right_user_self_write
                     ])

    await session.commit()


async def main():
    async with Session() as session:
        await create_default_role(session)

if __name__ == "__main__":
    asyncio.run(main())
