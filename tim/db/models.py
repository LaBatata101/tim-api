from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    is_admin = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, name={self.name}, email={self.email}, is_admin={self.is_admin},"
            f" hashed_password={self.hashed_password}, items={self.items})"
        )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(240), index=True, default=None)
    bar_code = Column(String(13), index=True)
    price = Column(DECIMAL(10, 2), index=True)
    image_path = Column(String, default=None)
    quantity = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return (
            f"Item(id={self.id}, title={self.title}, description={self.description}, price={self.price},"
            f" image_path={self.image_path}, owner={self.owner_id})"
        )
