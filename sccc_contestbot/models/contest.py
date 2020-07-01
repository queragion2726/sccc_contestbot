from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class Contest(Base):
    __tablename__ = "contests"

    id = Column(String(64), primary_key=True)
    contest_name = Column(String(128))
    start_date = Column(DateTime)
    URL = Column(String(512))

    def __repr__(self):
        return f"Contest<(id={self.id}, contest_name={self.contest_name}, start_date={self.start_date})>"

