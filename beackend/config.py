import os
from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    USER_NAME = os.getenv("USER_NAME")
    PASSWORD = os.getenv("PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    def get_connection(self):
        CONNECTION_URL = (f"postgresql://{self.USER_NAME}"
                          f":{self.PASSWORD}"
                          f"@localhost:5432/{self.DB_NAME}")
        return CONNECTION_URL
