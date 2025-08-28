from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.beackend.database import Base


class Connection:
    _connection = None
    def __new__(cls, connection_string:str):
        if cls._connection is None:
            cls._connection = super().__new__(cls)
            cls._connection.engin = create_engine(connection_string, echo=False)
            cls._connection.Session = sessionmaker(bind=cls._connection.engin)
            Base.metadata.drop_all(cls._connection.engin)
            Base.metadata.create_all(cls._connection.engin)

    def get_connection(self) -> sessionmaker:
        return self.Session
