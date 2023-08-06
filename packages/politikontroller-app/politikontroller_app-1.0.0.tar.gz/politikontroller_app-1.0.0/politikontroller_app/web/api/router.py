from fastapi.routing import APIRouter

from politikontroller_app.web.api import monitoring, user, police_controls

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(user.router, prefix='/user')
api_router.include_router(police_controls.router, prefix='/police_controls')
