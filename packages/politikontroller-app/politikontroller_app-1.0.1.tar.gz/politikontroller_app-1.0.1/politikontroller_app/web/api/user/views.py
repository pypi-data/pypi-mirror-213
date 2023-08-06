""" User routes """

from logging import getLogger
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from requests import HTTPError
from sqlalchemy.ext.asyncio import AsyncSession

from politikontroller_py import Client
from politikontroller_py.exceptions import AuthenticationError
from politikontroller_py.models import Account
from politikontroller_app.shared.dependencies import (
    get_current_active_user,
    get_db_session,
)
from politikontroller_app.db.dao import Auth


router = APIRouter()
_LOGGER = getLogger(__name__)

client = Client()


@router.post("/token")
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db_session),
):
    dao = Auth(db)
    try:
        user = client.authenticate_user(form_data.username, form_data.password)
    except HTTPError as err:
        raise HTTPException(403, detail=str(err)) from err
    except AuthenticationError as err:
        raise HTTPException(403) from err

    # user = User(**user_dict)
    token = dao.create_access_token(user.username, form_data.password)

    return {"access_token": token.token, "token_type": "bearer"}


@router.get("/settings")
async def user_settings(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    client.set_user(current_user)
    settings = client.get_settings()
    return settings


@router.get("/maps")
async def user_maps(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    client.set_user(current_user)
    maps = client.get_maps()
    return maps


@router.get("/points")
async def user_exchange_points(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    client.set_user(current_user)
    res = client.exchange_points()
    return res
