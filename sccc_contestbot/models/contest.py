import datetime
from hashlib import md5

from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True)
    contest_id = Column(String(32), unique=True)
    contest_name = Column(String(128))
    start_date = Column(DateTime)
    URL = Column(String(512))
    hash_value = Column(String(32))

    __mapper_args__ = {
        "confirm_deleted_rows": False,
    }

    def __init__(
        self,
        contest_id: str,
        contest_name: str,
        start_date: datetime.datetime,
        URL: str,
    ):
        self.contest_id = contest_id
        self.contest_name = contest_name
        self.start_date = start_date
        self.URL = URL

        hash_value = b""
        hash_value += contest_id.encode()
        hash_value += contest_name.encode()
        hash_value += str(start_date).encode()
        hash_value += URL.encode()
        self.hash_value = md5(hash_value).hexdigest()

    def __repr__(self):
        return f"Contest<(id={self.id}, contest_name={self.contest_name}, start_date={self.start_date})>"

