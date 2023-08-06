from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from politikontroller_app.db.base import Base


class AccessToken(Base):
    """Model for user access token."""

    __tablename__ = "access_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(length=100))
    username: Mapped[str] = mapped_column(String(length=20))
    password: Mapped[str] = mapped_column(String(length=100))
    disabled: bool = False
