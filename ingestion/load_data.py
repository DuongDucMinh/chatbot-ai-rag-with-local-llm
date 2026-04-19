# chia file json raw thành nhiều file json nhỏ theo từng bảng

import json
import logging
from pathlib import Path

from core.load_settings import load_settings
from core.setup_logging import setup_logging

setup_logging()
logger = logging.getLogger("ingestion")

settings = load_settings()
INPUT_PATH = Path(settings["data"]["raw_dir"]) # dùng Path để chuyển str -> Path
OUTPUT_PATH = Path(settings["data"]["processed_dir"])

def load_data():
    file_path = INPUT_PATH / "database_export_2026-01-23T02-02-46.json"
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Successfully loaded data from {file_path}")

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return []
    
    all_tables = data.get("tables", []) # Nếu không có value trong key "tables" thì trả về list rỗng
    
    for table_name, table_data in all_tables.items():
        if not table_data:
            logger.warning(f"Table {table_name} is empty")
            continue

        logger.info(f"Processing table: {table_name} with {len(table_data)} records")
        output_file = OUTPUT_PATH / f"{table_name}.json"

        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(table_data, out_file, ensure_ascii=False, indent=4) # indent=4 nghĩa là tab 4 lần để dễ đọc
            logger.info(f"Saved processed data to {output_file}")

if __name__ == "__main__":
    load_data()