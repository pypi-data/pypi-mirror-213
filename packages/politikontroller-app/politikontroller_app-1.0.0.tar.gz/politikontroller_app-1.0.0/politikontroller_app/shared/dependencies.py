""" Deps """
from typing import Annotated
from collections.abc import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from politikontroller_py.models import Account
from politikontroller_app.db.dao import Auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """ Create and get database session. """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    dao = Auth(db)
    token = await dao.get_by_token(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Account(username=token.username, password=token.password)


async def get_current_active_user(
    current_user: Annotated[Account, Depends(get_current_user)]
):
    return current_user
