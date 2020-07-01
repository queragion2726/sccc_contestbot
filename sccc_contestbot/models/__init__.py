from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .subscriber import Subscriber
from .contest import Contest
