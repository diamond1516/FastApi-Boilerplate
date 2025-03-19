__all__ = (
    'get_user_or_none',
    'get_active_user',
    'get_user_by_role',
    'user_or_none',
    'active_user',
)

from typing import Union, Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from managers.db.engine import get_db
from models import User
from utils.jwt import Payload
from .current_payload import get_token_payload_or_none, get_token_payload


async def get_user_or_none(
        db: Annotated[AsyncSession, Depends(get_db)],
        payload: Annotated[Payload, Depends(get_token_payload_or_none)],

) -> Union[User, None]:
    if payload:
        user = await User.repo.db_first(session=db, id=payload.id)

        if user:
            if user.is_active is False:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not active')

        return user


async def get_active_user(
        user: Annotated[User, Depends(get_user_or_none)],
):
    if user and user.is_active:
        return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

def get_user_by_role(**kwargs):
    async def role_checker(
            db: Annotated[AsyncSession, Depends(get_db)],
            payload: Annotated[Payload, Depends(get_token_payload)],
    ):
        user = await User.repo.db_first(session=db, id=payload.id, **kwargs)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user

    return role_checker


user_or_none = Annotated[User, Depends(get_user_or_none)]
active_user = Annotated[User, Depends(get_active_user)]
