from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

from .User import User
from .Item import Item