import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from models import Base


class Item(Base):
    __tablename__ = "item"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    category = sa.Column(sa.String)
    description = sa.Column(sa.String)

    user_id = sa.Column(GUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="items")