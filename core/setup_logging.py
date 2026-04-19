import yaml
import logging.config

def setup_logging():
    with open("config/logging.yaml", "r", encoding="utf-8") as file:
        # doc file yaml va chuyen sang python dict
        logging.config.dictConfig(yaml.safe_load(file))