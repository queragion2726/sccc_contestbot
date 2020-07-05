import datetime
from hashlib import md5

from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class ContestData:
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
        self.hash_value = None
        self.update_hash()

    def update_hash(self):
        source = b""
        source += self.contest_id.encode()
        source += self.contest_name.encode()
        source += str(self.start_date).encode()
        source += self.URL.encode()
        self.hash_value = md5(source).hexdigest()


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

    def __init__(self, data: ContestData):
        self.contest_id = data.contest_id
        self.contest_name = data.contest_name
        self.start_date = data.start_date
        self.URL = data.URL
        self.hash_value = data.hash_value

    def __repr__(self):
        return f"Contest<(id={self.id}, contest_name={self.contest_name}, start_date={self.start_date})>"

    def as_data(self) -> ContestData:
        return ContestData(
            self.contest_id, self.contest_name, self.start_date, self.URL
        )
