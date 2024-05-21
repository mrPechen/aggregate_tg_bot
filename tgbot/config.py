from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DbConfig:
    host: str
    db: str
    collection: str
    port: int

    def construct_mongo_url(self, host=None, port=None) -> str:

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = f"mongodb://{host}:{port}"
        return uri

    @staticmethod
    def from_env(env: Env):

        host = env.str("MONGO_HOST")
        db = env.str("MONGO_DB_NAME")
        collection = env.str("MONGO_COLLECTION_NAME")
        port = env.int("MONGO_PORT")
        return DbConfig(
            host=host, db=db, collection=collection, port=port)


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS", subcast=int)
        use_redis = False
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class Config:
    tg_bot: TgBot
    db: Optional[DbConfig] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        db=DbConfig.from_env(env)
    )
