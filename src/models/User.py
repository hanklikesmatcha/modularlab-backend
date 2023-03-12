import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from models import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    items = relationship("Item", back_populates="user")