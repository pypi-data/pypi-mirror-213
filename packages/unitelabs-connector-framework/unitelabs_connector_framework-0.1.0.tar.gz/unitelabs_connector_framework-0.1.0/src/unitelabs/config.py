import pydantic
import sila.server as sila
from sila import cloud_connector


class Config(pydantic.BaseSettings):
    environment: str = "development"
    sila_server: sila.ServerConfig = sila.ServerConfig()
    cloud_server_endpoint: cloud_connector.CloudServerEndpointConfig = cloud_connector.CloudServerEndpointConfig()

    class Config:
        env_file = ".env", ".env.prod"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
