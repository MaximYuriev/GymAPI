from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")


class MongoDBConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="MONGODB_")

    host: str
    port: str
    username: str
    password: str
    db_name: str

    @property
    def url(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"


class RMQConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="RMQ_")
    host: str
    port: str
    user: str
    password: str = Field(alias="RMQ_PASS")

    @property
    def rmq_url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class Config(BaseSettings):
    mongodb: MongoDBConfig = Field(default_factory=MongoDBConfig)
    rmq: RMQConfig = Field(default_factory=RMQConfig)


config = Config()
