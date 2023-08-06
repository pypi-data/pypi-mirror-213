from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models.access_token import AccessToken


class Auth:
    """Class for accessing access_token table."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def create_access_token(self, username: str, password: str) -> AccessToken:
        """ Add new token. """
        token = uuid4().hex

        access_token = AccessToken(username=username, password=password, token=token)
        self.session.add(access_token)
        #await self.session.commit()
        #await self.session.refresh(access_token)
        return access_token

    async def get_by_token(self, token: str) -> AccessToken:
        """ Get by access token. """
        query = select(AccessToken)
        query = query.where(AccessToken.token == token)

        result = await self.session.execute(query)
        return result.scalars().one_or_none()
