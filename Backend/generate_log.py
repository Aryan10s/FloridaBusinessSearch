import os
import yaml
import logging

config_path = os.getcwd()
config_details = yaml.safe_load(
    open(config_path + "/config/app_configurations.yaml"))

default_log_level = config_details["default_log_level"]

logging.basicConfig(filename=config_path + '/logs/engine.log',
                    level=logging.DEBUG,
                    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s -  %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.suffix = "%Y-%m-%d"
logger = logging.getLogger()
logger.setLevel(default_log_level)
