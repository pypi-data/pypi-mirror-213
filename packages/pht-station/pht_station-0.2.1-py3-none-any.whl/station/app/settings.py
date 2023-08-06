import functools
import json
import os
import re
from enum import Enum
from typing import Optional, Tuple, Union

from cryptography.fernet import Fernet
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, PostgresDsn, SecretStr, parse_obj_as
from yaml import safe_dump, safe_load

from station.app.env import StationEnvironmentVariables


class Emojis(str, Enum):
    """
    Enum of emojis to use in the app.
    """

    INFO = "ℹ️"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"


class RegistrySettings(BaseModel):
    address: Union[AnyHttpUrl, str]
    user: str
    password: SecretStr
    project: Optional[str] = None

    @property
    def api_url(self) -> str:
        """
        Returns the API URL of the registry.
        """
        if isinstance(self.address, str):
            if self.address.startswith("https://"):
                return self.address + "/api/v2.0"
            else:
                return "https://" + self.address + "/api/v2.0"
        else:
            return self.address + "/api/v2.0"


class AirflowSettings(BaseModel):
    host: Optional[Union[AnyHttpUrl, str]] = "airflow"
    # api_url: Optional[str] = "http://localhost:8080/api/v1/"
    port: Optional[int] = None
    user: Optional[str] = "admin"
    password: Union[SecretStr, str]
    station_db_dsn: Optional[PostgresDsn] = None

    @property
    def api_url(self) -> str:
        """
        Returns the API URL of Airflow.
        """
        if isinstance(self.host, str):
            if self.host.startswith("http://") or self.host.startswith("https://"):
                api_url = self.host + (f":{self.port}" if self.port else "")
            else:
                api_url = f"http://{self.host}" + f":{self.port}" if self.port else ""

        elif isinstance(self.host, AnyHttpUrl):
            url = "http://" + self.host.host + f":{self.port}" if self.port else ""
            api_url = url + self.host.path if self.host.path else ""
        else:
            raise ValueError("Airflow host is not a valid URL.")
        if not api_url.endswith("/api/v1/"):
            if api_url.endswith("/"):
                api_url += "api/v1/"
            else:
                api_url += "/api/v1/"
        return api_url


class MinioSettings(BaseModel):
    host: Optional[Union[AnyHttpUrl, AnyUrl, str]] = "minio"
    port: Optional[int] = None
    access_key: str
    secret_key: Union[SecretStr, str]

    @property
    def server_url(self) -> str:
        """
        Returns the server URL of Minio.
        """
        return f"{self.host}{':' + str(self.port) if self.port else ''}"


class CentralUISettings(BaseModel):
    api_url: Optional[AnyHttpUrl] = None
    robot_id: Optional[str] = None
    robot_secret: Optional[SecretStr] = None


class RedisSettings(BaseModel):
    host: Optional[str] = "redis"
    port: Optional[int] = 6379
    password: Optional[SecretStr] = None
    db: Optional[int] = 0


class AuthConfig(BaseModel):
    robot_id: str
    robot_secret: SecretStr
    host: Optional[Union[AnyHttpUrl, AnyUrl, str]] = "station-auth"
    port: Optional[int] = None

    @property
    def token_url(self) -> str:
        if self.host.startswith("http") or self.host.startswith("https"):
            return f"{self.host}{f':{self.port}' if self.port else ''}/token"
        return f"http://{self.host}{f':{self.port}' if self.port else ''}/token"

    @property
    def user_url(self) -> str:
        if self.host.startswith("http") or self.host.startswith("https"):
            return f"{self.host}{f':{self.port}' if self.port else ''}/users"
        return f"http://{self.host}{f':{self.port}' if self.port else ''}/users"

    @property
    def auth_url(self) -> Union[AnyUrl, str]:
        if self.host.startswith("http") or self.host.startswith("https"):
            return f"{self.host}{f':{self.port}' if self.port else ''}"
        return f"http://{self.host}{f':{self.port}' if self.port else ''}"


class StationRuntimeEnvironment(str, Enum):
    """
    Enum of the runtime environments of the station.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class DatabaseSettings(BaseModel):
    admin_user: str
    admin_password: str
    host: Optional[str] = "postgres"
    port: Optional[int] = 5432
    database: Optional[str] = "pht_station"

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn(
            scheme="postgresql+psycopg2",
            user=self.admin_user,
            password=self.admin_password,
            url=self.host,
            port=self.port,
            path=f"/{self.database}",
        )

    @classmethod
    def from_dsn(cls, dsn: PostgresDsn):
        return cls(
            admin_user=dsn.user,
            admin_password=dsn.password,
            host=dsn.host,
            port=dsn.port,
            database=dsn.path,
        )


class StationConfig(BaseModel):
    """
    Object containing the configuration of the station.
    """

    station_id: Union[int, str]
    station_data_dir: Optional[str]
    host: Optional[Union[AnyHttpUrl, str]] = os.getenv(
        StationEnvironmentVariables.STATION_API_HOST.value, "0.0.0.0"
    )
    port: Optional[int] = os.getenv(
        StationEnvironmentVariables.STATION_API_PORT.value, 8000
    )
    db: DatabaseSettings
    environment: Optional[
        StationRuntimeEnvironment
    ] = StationRuntimeEnvironment.DEVELOPMENT
    fernet_key: Optional[SecretStr] = None
    registry: RegistrySettings
    auth: Optional[AuthConfig] = None
    airflow: Optional[AirflowSettings] = None
    minio: Optional[MinioSettings] = None
    central_ui: Optional[CentralUISettings] = CentralUISettings()
    redis: Optional[RedisSettings] = RedisSettings()

    @classmethod
    def from_file(cls, path: str) -> "StationConfig":
        """
        Parse the application configuration file (station_config.yml) for the settings required to run the station api.
        Args:
            path: location of the configuration file

        Returns:
            StationConfig object containing the configuration of the station api.
        """

        return cls._parse_config_file(path)

    @staticmethod
    def _parse_config_file(path: str) -> "StationConfig":
        with open(path, "r") as f:
            config_dict = safe_load(f)

        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            config_dict["db"]["admin_user"],
            config_dict["db"]["admin_password"],
            config_dict["db"].get("host", "postgres"),
            config_dict["db"].get("port", 5432),
            config_dict["db"].get("database", "pht_station"),
        )

        db = DatabaseSettings(
            admin_user=config_dict["db"]["admin_user"],
            admin_password=config_dict["db"]["admin_password"],
            host=config_dict["db"].get("host", "postgres"),
            port=config_dict["db"].get("port", 5432),
            database=config_dict["db"].get("database", "pht_station"),
        )

        registry_settings = RegistrySettings(
            address=config_dict["registry"]["address"],
            user=config_dict["registry"]["user"],
            password=config_dict["registry"]["password"],
            project=config_dict["registry"].get("project", None),
        )

        auth_settings = AuthConfig(
            robot_id=config_dict["auth"]["robot_id"],
            robot_secret=config_dict["auth"]["robot_secret"],
            host=config_dict["auth"].get("host", "station-auth"),
            port=config_dict["auth"].get("port", 3010),
        )

        airflow_settings = AirflowSettings(
            host=config_dict.get("airflow").get("host", "airflow"),
            port=config_dict.get("airflow").get("port", 8080),
            user=config_dict.get("airflow").get("admin_user", "admin"),
            password=config_dict.get("airflow").get("admin_password"),
        )
        # airflow_settings.api_url = f"http://{airflow_settings.host}:{airflow_settings.port}/api/v1/"

        minio_settings = MinioSettings(
            host=config_dict.get("minio").get("host", "minio"),
            port=config_dict.get("minio").get("port", 9000),
            access_key=config_dict.get("minio").get("admin_user", "minio_admin"),
            secret_key=config_dict.get("minio").get("admin_password"),
        )

        central_settings = CentralUISettings(
            api_url=config_dict.get("central").get("api_url"),
            robot_id=config_dict.get("central").get("robot_id"),
            robot_secret=config_dict.get("central").get("robot_secret"),
        )

        return StationConfig(
            station_id=config_dict["station_id"],
            station_data_dir=config_dict["station_data_dir"],
            host=os.getenv(
                str(StationEnvironmentVariables.STATION_API_HOST.value), "0.0.0.0"
            ),
            port=os.getenv(
                str(StationEnvironmentVariables.STATION_API_PORT.value), 8000
            ),
            db=db,
            environment=StationRuntimeEnvironment(config_dict["environment"]),
            fernet_key=config_dict["api"]["fernet_key"],
            registry=registry_settings,
            auth=auth_settings,
            airflow=airflow_settings,
            minio=minio_settings,
            central_ui=central_settings,
            redis=RedisSettings(),
        )

    def to_file(self, path: str) -> None:
        # todo get secret values recursively
        with open(path, "w") as f:
            safe_dump(json.loads(self.json(indent=2)), f)


# https://stackoverflow.com/a/31174427/3838313
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


# Evaluation for initialization of values file < environment
class Settings:
    """
    Class to handle the settings of the station API and connections to other services. Can be configured via a file or
    environment variables.
    """

    config: StationConfig
    config_path: Optional[str]
    is_initialized: bool

    def __init__(self, config_path: str = None, config: StationConfig = None):
        load_dotenv(find_dotenv())
        self._config_file = False
        self.config = None
        self.is_initialized = False
        if config:
            self.config = config
        elif config_path:
            self.config_path = config_path
            self._config_file = True
        else:
            self.config_path = os.getenv(
                StationEnvironmentVariables.CONFIG_PATH.value, "station_config.yml"
            )
            self._config_file = True
        # todo create/update config file
        if os.getenv("ENVIRONMENT") == "development":
            self.setup()

    def setup(self) -> StationConfig:
        """
        Initialize the settings. First tries to load the settings from the config file. Then tries to load the settings
        from the environment variables. If a conflicting value is found the environment variable has precedence. If both
        fail, the default settings are used.

        Returns:
            StationConfig The initialized settings.

        """
        logger.info(f"{Emojis.INFO.value}Setting up station backend...")
        # check for config file at given or default path and load if exists
        self._check_config_path()
        # validate the runtime environment
        self._setup_runtime_environment()
        self._setup_station_environment()

        logger.info(f"Station backend setup successful {Emojis.SUCCESS.value}")
        self.is_initialized = True
        return self.config

    def get_fernet(self) -> Fernet:
        """
        Get the Fernet key for encryption and decryption of secrets. Configured via environment variables or station
        config.

        Returns: A fernet object that can be used to encrypt and decrypt secrets.
        """
        if self.config.fernet_key is None:
            raise ValueError("No Fernet key provided")

        key = str(self.config.fernet_key)
        return Fernet(key.encode())

    def _check_config_path(self):
        """
        Checks if a config is present at the given path. Raise an error if custom config file is given but not present.

        Returns:

        """
        print(os.getcwd())
        logger.info(f"{Emojis.INFO.value}Looking for config file...")
        print("Config path", self.config_path)
        if not os.path.isfile(self.config_path):
            if self.config_path == "station_config.yml":
                logger.warning(
                    f"\t{Emojis.WARNING.value} "
                    f"No config file found. Attempting configuration via environment variables..."
                )
            else:
                raise FileNotFoundError(
                    f"{Emojis.ERROR.value}   Custom config file not found at {self.config_path}."
                )
            # construct a placeholder config to fill with environment and default values
            self.config = StationConfig.construct()
        # Parse the config file
        else:
            logger.info(
                f"\t{Emojis.SUCCESS.value}   Config file found at {self.config_path} loading... "
            )
            config = StationConfig.from_file(self.config_path)
            print(config)
            self.config = config
            logger.info(f"{Emojis.SUCCESS.value} Config loaded.")

    def _setup_runtime_environment(self):
        """
        Setup and validate the runtime environment (development|production) of the station API
        Returns:

        """
        environment_var = os.getenv(StationEnvironmentVariables.ENVIRONMENT.value)
        # if config variable is in environment variables use it
        if environment_var:
            try:
                runtime_environment = StationRuntimeEnvironment(environment_var)
                # display when config variable is overwritten with env var
                if self.config.environment:
                    logger.debug(
                        f"{Emojis.INFO.value}Overriding runtime environment with env var specification."
                    )
            except ValueError:
                raise ValueError(
                    f"{Emojis.ERROR.value}   Invalid value ({environment_var}) for runtime environment"
                    f" in env var {StationEnvironmentVariables.ENVIRONMENT.value}."
                )
        # otherwise, use the value parse from config file
        else:
            runtime_environment = self.config.environment

        # Display runtime environment
        if runtime_environment == StationRuntimeEnvironment.PRODUCTION:
            logger.info(f"{Emojis.INFO.value}Running in production environment.")
        elif runtime_environment == StationRuntimeEnvironment.DEVELOPMENT:
            logger.warning(
                f"{Emojis.WARNING.value}Development environment detected,"
                f" set environment variable '{StationEnvironmentVariables.ENVIRONMENT.value}' "
                f"to '{StationRuntimeEnvironment.PRODUCTION.value}' for production mode."
            )
        # set the parsed runtime environment
        self.config.environment = runtime_environment

    def _setup_station_environment(self):
        """
        After potential config files are found, parse the environment variables to override the config file values if
        they exist.
        Validate the configuration from both options.

        Returns:

        """

        # ensure that the station id is set
        env_station_id = os.getenv(StationEnvironmentVariables.STATION_ID.value)

        if not env_station_id:
            try:
                # todo improve this
                pass
            except AttributeError:
                raise ValueError(
                    f"{Emojis.ERROR.value}   No station id specified in config or env var "
                    f"{StationEnvironmentVariables.STATION_ID.value}."
                )
        elif env_station_id:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding station id with env var specification."
            )
            self.config.station_id = env_station_id

        # parse environment variables
        self._setup_station_api()
        self._setup_central_api_connection()
        self._setup_airflow()
        self._setup_fernet()
        self._setup_station_auth()
        self._setup_redis()
        self._setup_registry_connection()
        self._setup_minio_connection()

    def _setup_station_api(self):
        """
        Configure the station api url, port and database connection from environment variables or config file.
        Returns:

        """
        # Try to find api host and port in environment variables
        env_station_host = os.getenv(StationEnvironmentVariables.STATION_API_HOST.value)
        if env_station_host:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding station api host with env var specification."
            )
            self.config.host = env_station_host
        env_station_port = os.getenv(StationEnvironmentVariables.STATION_API_PORT.value)
        if env_station_port:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding station api port with env var specification."
            )
            self.config.port = int(env_station_port)
        station_db = os.getenv(StationEnvironmentVariables.STATION_DB.value)
        if station_db:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding station db with env var specification."
            )
            self.config.db = DatabaseSettings.from_dsn(
                parse_obj_as(PostgresDsn, station_db)
            )
        else:
            if self.config.environment == "production":
                raise ValueError(
                    f"{Emojis.ERROR.value} Connection string to station database needs to be specified in"
                    f" environment variables."
                )
            else:
                logger.warning(
                    f"{Emojis.WARNING.value} Connection string to station database is not specified in"
                    f" environment variables. Default database is used."
                )
        station_data_dir = os.getenv(StationEnvironmentVariables.STATION_DATA_DIR.value)
        if station_data_dir:
            self.config.station_data_dir = station_data_dir

        # if "sqlite" in self.config.db.dsn.lower():
        #     if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
        #         raise ValueError(f"{Emojis.ERROR.value}   SQLite database not supported for production mode.")
        #     else:
        #         logger.warning(f"{Emojis.WARNING.value}   SQLite database only supported in development mode.")

    def _setup_central_api_connection(self):
        self._validate_config_item(
            env_var=StationEnvironmentVariables.CENTRAL_API_URL,
            config_item="central_ui.api_url",
        )
        self._validate_config_item(
            env_var=StationEnvironmentVariables.STATION_ROBOT_ID,
            config_item="central_ui.robot_id",
        )
        self._validate_config_item(
            env_var=StationEnvironmentVariables.STATION_ROBOT_SECRET,
            config_item="central_ui.robot_secret",
        )

        logger.info(
            f"{Emojis.INFO.value} Central API url: {self.config.central_ui.api_url}, "
            f"Robot ID: {self.config.central_ui.robot_id} Robot Secret: ******"
        )

    def _validate_config_item(
        self,
        env_var: StationEnvironmentVariables,
        config_item: str,
        error_message: str = None,
        warning_message: str = None,
        item_name: str = None,
    ):
        """
        Validates that a config item is present in the environment variables. If not, a warning or error is raised.
        Args:
            env_var: the environment variable the item can be found in
            config_item: attr path of the station configuration of the item
            error_message: optional custom error message
            warning_message: optional custom warning message
            item_name: optional display name of the item in the error messages

        Returns:

        """
        env_var = os.getenv(env_var.value)
        if env_var:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding {item_name if item_name else config_item} with env var specification."
            )
            rsetattr(self.config, config_item, env_var)
        elif rgetattr(self.config, config_item):
            logger.debug(
                f"\t{Emojis.INFO.value}{item_name if item_name else config_item}: {rgetattr(self.config, config_item)}"
            )
        else:
            if self.config.environment == "production":
                if error_message:
                    raise ValueError(f"{Emojis.ERROR.value}{error_message}")
                else:
                    raise ValueError(
                        f"{Emojis.ERROR.value} {item_name if item_name else config_item} needs to be specified."
                    )
            else:
                if warning_message:
                    logger.warning(f"{Emojis.WARNING.value}{warning_message}")
                else:
                    logger.warning(
                        f"{Emojis.WARNING.value} {item_name if item_name else config_item} is not specified."
                    )

    def _setup_fernet(self):
        """
        Configure the fernet key from environment variables or config file.
        In the development mode if none is given generate a new one.
        Raise an error if no key is given in production mode.
        Returns:

        """
        env_fernet_key = os.getenv(str(StationEnvironmentVariables.FERNET_KEY.value))

        if not env_fernet_key and not self.config.fernet_key:
            # if fernet key is given in production raise an error
            if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
                raise ValueError(
                    f"{Emojis.ERROR.value}   No fernet key specified in config or env vars."
                )
            # generate new key in development mode
            elif self.config.environment == StationRuntimeEnvironment.DEVELOPMENT:
                logger.warning(
                    f"\t{Emojis.WARNING.value}No fernet key specified in config or env vars"
                )
                self.config.fernet_key = Fernet.generate_key().decode()
                logger.info(
                    f"\t{Emojis.INFO.value}Generated new key for development environment."
                )
        elif env_fernet_key and self.config.fernet_key:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding fernet key with env var specification."
            )
            self.config.fernet_key = env_fernet_key

        elif env_fernet_key:
            self.config.fernet_key = env_fernet_key

    def _setup_redis(self):
        """
        Configure the redis connection from environment variables or config file.
        Returns:

        """

        logger.info(f"{Emojis.INFO.value}Setting up redis connection...")
        redis_config = self.config.redis.copy()

        host = os.getenv(str(StationEnvironmentVariables.REDIS_HOST.value))
        port = os.getenv(str(StationEnvironmentVariables.REDIS_PORT.value))
        db = os.getenv(str(StationEnvironmentVariables.REDIS_DB.value))
        password = os.getenv(str(StationEnvironmentVariables.REDIS_PW.value))

        if host:
            logger.debug(
                f"\t{Emojis.INFO.value}Overriding redis connections with env var specification."
            )
            if not redis_config:
                redis_config = RedisSettings()
            redis_config.host = host
            redis_config.port = port or redis_config.port
            redis_config.db = db
            redis_config.password = password
            self.config.redis = redis_config
        if not self.config.redis:
            self.config.redis = RedisSettings()
            logger.info(
                f"\t{Emojis.INFO.value}No redis connection specified in config or env vars. Using default."
                f" Host: {self.config.redis.host}, Port: {self.config.redis.port}"
            )

    def _setup_station_auth(self):
        """
        Configure the connection to the station auth from environment variables or config file.
        Optional in development mode, raises an error if not configured in production mode.
        Returns:

        """
        logger.info(f"{Emojis.INFO.value}Setting up station authentication...")
        # check if station auth is configured via environment variables
        (
            env_auth_server,
            env_auth_port,
            env_auth_robot,
            env_auth_robot_secret,
        ) = self._get_internal_service_env_vars(
            host=StationEnvironmentVariables.AUTH_SERVER_HOST,
            port=StationEnvironmentVariables.AUTH_SERVER_PORT,
            user=StationEnvironmentVariables.AUTH_ROBOT_ID,
            secret=StationEnvironmentVariables.AUTH_ROBOT_SECRET,
        )

        _auth_server = False
        # ensure there is an auth server specified in production mode
        if not (
            (env_auth_server and env_auth_robot and env_auth_robot_secret)
            or self.config.auth
        ):
            if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
                raise ValueError(
                    f"{Emojis.ERROR.value}   No station auth specified in config or env vars,"
                    f" invalid configuration for production"
                )

        # no auth config present at initialization, create a new one
        elif not self.config.auth and (
            env_auth_server and env_auth_robot and env_auth_robot_secret
        ):
            logger.debug(
                f"{Emojis.INFO.value}No auth config found, creating new one from env vars."
            )
            env_auth_config = AuthConfig(
                host=env_auth_server,
                port=env_auth_port,
                robot_id=env_auth_robot,
                robot_secret=SecretStr(env_auth_robot_secret),
            )

            self.config.auth = env_auth_config
            _auth_server = True
        # if config and env vars exist override the config values with the environment variables
        elif self.config.auth and (
            env_auth_server or env_auth_robot or env_auth_robot_secret or env_auth_port
        ):
            logger.debug("Overriding auth server config with env var specifications.")
            if env_auth_server:
                self.config.auth.host = env_auth_server
            if env_auth_port:
                self.config.auth.port = env_auth_port
            if env_auth_robot:
                self.config.auth.robot_id = env_auth_robot
            if env_auth_robot_secret:
                self.config.auth.robot_secret = env_auth_robot_secret
            # validate the overridden config
            self.config.auth = AuthConfig(**self.config.auth.dict())
            _auth_server = True

        # log authentication server config and status
        if _auth_server:
            logger.info(
                f"Auth server: url - {self.config.auth.host}:{self.config.auth.port},"
                f" robot - {self.config.auth.robot_id}"
            )
        else:
            logger.warning(
                f"{Emojis.WARNING.value}No auth server specified in config or env vars,"
                f" ignoring in development mode"
            )

    def _setup_registry_connection(self):
        """
        Configure the connection to the central container registry from environment variables or config file.
        Raises an error if not configured in production mode.
        Returns:

        """
        logger.info(f"{Emojis.INFO.value}Setting up registry connection...")
        (
            env_registry,
            env_registry_user,
            env_registry_password,
        ) = self._get_external_service_env_vars(
            url=StationEnvironmentVariables.REGISTRY_URL,
            client_id=StationEnvironmentVariables.REGISTRY_USER,
            client_secret=StationEnvironmentVariables.REGISTRY_PW,
        )

        # catch attribute error if no registry config is present in config
        try:
            registry_config = self.config.registry
        except AttributeError:
            registry_config = None
        _registry_config = False
        # override registry config if env vars are present and validate afterwards
        if registry_config and (
            env_registry and env_registry_user and env_registry_password
        ):
            logger.debug("Overriding registry config with env var specifications.")
            if env_registry:
                registry_config.address = env_registry
            if env_registry_user:
                registry_config.user = env_registry_user
            if env_registry_password:
                registry_config.password = env_registry_password
            # validate the overridden config
            registry_config = RegistrySettings(**registry_config.dict())
        # no registry config found
        elif not registry_config and not (
            env_registry and env_registry_user and env_registry_password
        ):
            _registry_config = False
        elif not registry_config and (
            env_registry and env_registry_user and env_registry_password
        ):
            logger.debug(
                f"{Emojis.INFO.value}No registry config found, creating new one from env vars."
            )
            registry_config = RegistrySettings(
                address=env_registry,
                user=env_registry_user,
                password=env_registry_password,
            )
            self.config.registry = registry_config
            self._validate_config_item(
                StationEnvironmentVariables.REGISTRY_PROJECT,
                "registry.project",
            )
        # log registry config and status
        if registry_config:
            logger.info(
                f"Registry: url - {self.config.registry.address}, user - {self.config.registry.user}, "
                f"project - {self.config.registry.project}"
            )
        else:
            # raise error if no registry is configured in production mode
            if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
                raise ValueError(
                    f"{Emojis.ERROR.value}   No registry config specified in config or env vars"
                )
            else:
                logger.warning(
                    "No registry config specified in config or env vars, ignoring in development mode"
                )

    def _setup_minio_connection(self):
        """
        Configure the connection to the minio storage from environment variables or config file.
        Raises an error if not configured in production mode.
        Returns:

        """
        logger.info("Setting up minio connection...")
        # get the environment variables for minio
        env_connection = self._get_internal_service_env_vars(
            host=StationEnvironmentVariables.MINIO_HOST,
            port=StationEnvironmentVariables.MINIO_PORT,
            user=StationEnvironmentVariables.MINIO_ACCESS_KEY,
            secret=StationEnvironmentVariables.MINIO_SECRET_KEY,
        )
        (
            env_minio_host,
            env_minio_port,
            env_minio_access_key,
            env_minio_secret_key,
        ) = env_connection

        # get minio from config file or construct dummy
        _minio_config = False
        minio_config = self.config.minio
        if minio_config:
            _minio_config = True
            logger.debug("Minio config found, checking for env vars.")
        else:
            minio_config = MinioSettings.construct()

        # override minio config if config and env vars are present and validate afterwards
        if _minio_config and (
            env_minio_host
            or env_minio_port
            or env_minio_access_key
            or env_minio_secret_key
        ):
            logger.debug("Overriding minio config with env var specifications.")
            if env_minio_host:
                minio_config.host = env_minio_host
            if env_minio_port:
                minio_config.port = env_minio_port
            if env_minio_access_key:
                minio_config.access_key = env_minio_access_key
            if env_minio_secret_key:
                minio_config.secret_key = env_minio_secret_key
            _minio_config = True
        # no minio config found
        elif not _minio_config and not (
            env_minio_host and env_minio_access_key and env_minio_secret_key
        ):
            _minio_config = False

        # no config but environment variables are found
        elif not _minio_config and (
            env_minio_host and env_minio_access_key and env_minio_secret_key
        ):
            logger.debug(
                f"{Emojis.INFO.value}No minio config found, creating new one from env vars."
            )
            minio_config.host = env_minio_host
            minio_config.access_key = env_minio_access_key
            minio_config.secret_key = env_minio_secret_key
            if env_minio_port:
                minio_config.port = env_minio_port
            _minio_config = True

        # log minio config and status
        if _minio_config:
            # validate the overridden config
            self.config.minio = MinioSettings(**minio_config.dict())
            logger.info(
                f"Minio: host - {self.config.minio.host}, port - {self.config.minio.port}"
            )
        else:
            # raise error if no minio is configured in production mode
            if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
                raise ValueError(
                    f"{Emojis.ERROR}   No minio config specified in config or env vars"
                )
            else:
                logger.warning(
                    "No minio config specified in config or env vars, ignoring in development mode"
                )

    def _setup_airflow(self):
        logger.info(
            "Setting up airflow connection and airflow-connection to station database..."
        )

        # get the environment variables for airflow
        (
            env_airflow_api_url,
            env_airflow_port,
            env_airflow_user,
            env_airflow_secret,
        ) = self._get_internal_service_env_vars(
            host=StationEnvironmentVariables.AIRFLOW_API_URL,
            port=StationEnvironmentVariables.AIRFLOW_PORT,
            user=StationEnvironmentVariables.AIRFLOW_USER,
            secret=StationEnvironmentVariables.AIRFLOW_PW,
        )

        # get airflow from config file or construct dummy
        _airflow_config = False
        airflow_config = self.config.airflow
        if airflow_config:
            _airflow_config = True
            logger.debug("Airflow config found, checking for env vars.")
        else:
            airflow_config = AirflowSettings.construct()

        # override airflow config if config and env vars are present and validate afterwards
        if _airflow_config and (
            env_airflow_api_url
            or env_airflow_port
            or env_airflow_user
            or env_airflow_secret
        ):
            logger.debug("Overriding airflow config with env var specifications.")
            if env_airflow_api_url:
                airflow_config.host = env_airflow_api_url
            if env_airflow_port:
                airflow_config.port = env_airflow_port
            if env_airflow_user:
                airflow_config.user = env_airflow_user
            if env_airflow_secret:
                airflow_config.password = env_airflow_secret
            _airflow_config = True
        # no airflow config found
        elif not _airflow_config and not (
            env_airflow_api_url and env_airflow_user and env_airflow_secret
        ):
            _airflow_config = False

        # no config but environment variables are found
        elif not _airflow_config and (
            env_airflow_api_url and env_airflow_user and env_airflow_secret
        ):
            logger.debug(
                f"{Emojis.INFO.value}No airflow config found, creating new one from env vars."
            )
            airflow_config.host = env_airflow_api_url.split("://")[1]
            if re.search(r":\d+", env_airflow_api_url):
                airflow_config.port = (
                    re.search(r":\d+", env_airflow_api_url).group(0).replace(":", "")
                )
            airflow_config.user = env_airflow_user
            airflow_config.password = env_airflow_secret
            if env_airflow_port:
                airflow_config.port = env_airflow_port
            _airflow_config = True

        # log airflow config and status
        if _airflow_config:
            # validate the overridden config
            self.config.airflow = AirflowSettings(**airflow_config.dict())
            logger.info(
                f"Airflow: API url - {self.config.airflow.api_url}, port - {self.config.airflow.port}"
            )
        else:
            # raise error if no airflow is configured in production mode
            if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
                raise ValueError(
                    f"{Emojis.ERROR.value}   No airflow config specified in config or env vars"
                )
            else:
                logger.warning(
                    "No airflow config specified in config or env vars, generating defaults for "
                    "development mode"
                )
                self.config.airflow = AirflowSettings()

        # todo re-enable this when checked if it is necessary -> should probably just use api calls to station api
        # # Check whether connection to station database with connection_id already exists, if not create it
        # try:
        #     self._create_station_db_connection()
        # except Exception as e:
        #     logger.error(f"{Emojis.ERROR}   Could not create airflow connection to station database: {e}")
        #     if self.config.environment == StationRuntimeEnvironment.PRODUCTION:
        #         raise ValueError(f"{Emojis.ERROR.value}   Unable to add database connection to airflow")
        #     else:
        #         logger.warning(f"Unable to add database connection to airflow. Is airflow running?")
        #         logger.error(e)

    # def _create_station_db_connection(self):
    #
    #     connection_id = "pg_station"
    #     self.config.airflow.station_db_dsn = self.config.db.dsn
    #     if isinstance(self.config.db, str):
    #         credentials, host = self.config.db.split("://")[1].split("@")
    #     elif isinstance(self.config.db, SecretStr):
    #         credentials, host = (
    #             self.config.db.get_secret_value().split("://")[1].split("@")
    #         )
    #     else:
    #         raise ValueError(
    #             f"{Emojis.ERROR.value.value}   Unable to parse database connection string"
    #         )
    #     user, password = credentials.split(":")
    #     host, schema = host.split("/")
    #     port = 5432
    #     if len(host.split(":")) == 2:
    #         host, port = host.split(":")
    #         port = int(port)
    #
    #     conn = {
    #         "connection_id": connection_id,
    #         "conn_type": "postgres",
    #         "host": "postgres",
    #         "login": user,
    #         "port": port,
    #         "password": password,
    #         "schema": schema,
    #     }
    #
    #     # Check whether connection with connection_id already exists, if not create it
    #     url_get = self.config.airflow.api_url + f"connections/{connection_id}"
    #     url_post = self.config.airflow.api_url + "connections"
    #     auth = HTTPBasicAuth(
    #         self.config.airflow.user, self.config.airflow.password.get_secret_value()
    #     )
    #     r = requests.get(url=url_get, auth=auth, verify=False)
    #
    #     if r.status_code != 200:
    #         logger.debug(
    #             f"\t{Emojis.INFO}Database connection in airflow with connection id {connection_id} does not exist,"
    #             f" creating new one from environment variables."
    #         )
    #         try:
    #             r = requests.post(url=url_post, auth=auth, json=conn, verify=False)
    #             r.raise_for_status()
    #             logger.info(
    #                 f"\t{Emojis.INFO} Database connection in airflow with id {connection_id} got created."
    #             )
    #         except Exception as e:
    #             f"\t{Emojis.WARNING}Error occured while trying to create the database connection "
    #             f"in airflow with id " f"{connection_id}."
    #             f"\t{Emojis.WARNING} -- {e}."
    #     else:
    #         logger.info(
    #             f"\t{Emojis.INFO} Database connection in airflow with id {connection_id} exists."
    #        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"

    @staticmethod
    def _get_external_service_env_vars(
        url: StationEnvironmentVariables,
        client_id: StationEnvironmentVariables,
        client_secret: StationEnvironmentVariables,
    ) -> Tuple[str, str, str]:
        """
        Get the tuple of connection variables for an external service from environment variables.
        Args:
            url:
            client_id:
            client_secret:

        Returns:

        """
        env_url = os.getenv(url.value)
        env_client_id = os.getenv(client_id.value)
        env_client_secret = os.getenv(client_secret.value)
        return env_url, env_client_id, env_client_secret

    @staticmethod
    def _get_internal_service_env_vars(
        host: StationEnvironmentVariables,
        port: StationEnvironmentVariables,
        user: StationEnvironmentVariables,
        secret: StationEnvironmentVariables,
    ) -> Tuple[str, int, str, str]:
        """
        Get the tuple of connection variables for an internal service from environment variables.
        Args:
            host:
            port:
            user:
            secret:

        Returns:

        """
        env_server_host = os.getenv(host.value)
        env_server_port = os.getenv(port.value)
        if env_server_port:
            env_server_port = int(env_server_port)
        env_server_user = os.getenv(user.value)
        env_server_secret = os.getenv(secret.value)
        return env_server_host, env_server_port, env_server_user, env_server_secret


settings = Settings()
