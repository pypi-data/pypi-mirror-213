import configparser
import os
from pathlib import Path

from loguru import logger


class Config:
    def __init__(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent
        config = configparser.ConfigParser()
        DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "PROD")
        logger.info(f"Read {DEPLOYMENT_MODE} config")
        config.read(f"{BASE_DIR}/configs/config-{DEPLOYMENT_MODE.lower()}.ini")

        self.API_PREFIX: str = "/api/v2"
        self.IP: str = config["GENERAL"]["IP"]
        self.PORT: int = int(config["GENERAL"]["PORT"])
