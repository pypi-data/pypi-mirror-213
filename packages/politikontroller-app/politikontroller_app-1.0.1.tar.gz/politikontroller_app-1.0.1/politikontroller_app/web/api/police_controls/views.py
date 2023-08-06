""" Police controls routes """

from logging import getLogger
from typing import Annotated
from fastapi import APIRouter, Depends
from geojson.mapping import to_mapping

from politikontroller_py.models import (
    Account,
    PoliceControl,
    PoliceControlType,
)
from politikontroller_py import Client
from politikontroller_app.shared.dependencies import (
    get_current_active_user,
)


router = APIRouter()
_LOGGER = getLogger(__name__)


@router.get("/", response_model=list[PoliceControl])
async def index(
    current_user: Annotated[Account, Depends(get_current_active_user)],
    geo_json: bool = False,
):
    client = Client(current_user)
    data = client.get_controls(63.1, 11.2)
    if geo_json:
        return {
            "type": "FeatureCollection",
            "features": [to_mapping(PoliceControl(**d)) for d in data],
        }
    return data


@router.get("/info/{control_id}", response_model=PoliceControl)
async def get_control(
    control_id: int,
    current_user: Annotated[Account, Depends(get_current_active_user)],
):
    client = Client(current_user)
    return client.get_control(control_id)


@router.get("/by-radius", response_model=list[PoliceControl] | dict)
async def by_radius(
    current_user: Annotated[Account, Depends(get_current_active_user)],
    radius: int,
    lat: float,
    lng: float,
    geo_json: bool = False,
):
    client = Client(current_user)
    data = client.get_controls(lat, lng, p='gps_kontroller', vr=radius, speed=100)
    if geo_json:
        return {
            "type": "FeatureCollection",
            "features": [to_mapping(PoliceControl(**d)) for d in data],
        }
    return data


@router.get("/types", response_model=list[PoliceControlType])
async def types(current_user: Annotated[Account, Depends(get_current_active_user)]):
    client = Client(current_user)
    return client.get_control_types()
