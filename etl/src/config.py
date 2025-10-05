from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()


class MySQLSettings(BaseModel):
    host: str = Field(default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    port: int = Field(default=int(os.getenv("MYSQL_PORT", "3306")))
    user: str = Field(default=os.getenv("MYSQL_USER", "root"))
    password: str = Field(default=os.getenv("MYSQL_PASSWORD", ""))
    database: str = Field(default=os.getenv("MYSQL_DB", "dw_ecommerce"))
    pool_size: int = Field(default=int(os.getenv("MYSQL_POOL_SIZE", "10")))
    pool_timeout: int = Field(default=int(os.getenv("MYSQL_POOL_TIMEOUT", "30")))

    def sqlalchemy_url(self) -> str:
        return (
            f"mysql+mysqlconnector://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


SOURCE_SETTINGS = MySQLSettings()
