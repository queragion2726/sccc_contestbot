from sqlalchemy import Column, Integer, String

from . import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    token = Column(String(32), unique=True)

    def __repr__(self):
        return f"<Subscriber(id={self.id}, token={self.token})>"

