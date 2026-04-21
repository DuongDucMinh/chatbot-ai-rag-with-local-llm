# chunking architecture types data thành nhiều chunk nhỏ (mỗi chunk là 1 record trong table architectureTypes)

import json
import logging
from pathlib import Path

from core.load_settings import load_settings
from core.setup_logging import setup_logging

setting = load_settings()
# setup_logging()
logger = logging.getLogger("ingestion")

def chunk_architecture_types():
    file_path = Path(setting["data"]["processed_dir"] / "architectureTypes.json")

    # Nếu đường dẫn file không tồn tại
    if not file_path.exists():
        logger.error(f"Input file not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Successfully loaded data from {file_path}")
    except Exception as e:
        logger.error(f"Error processing architecture types: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No architecture types found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"Architecture types data is not a list")
        return []
    
    chunks = []

    for idx, architecture_type in enumerate(data):
        if not isinstance(architecture_type, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        architecture_id = architecture_type.get("id")
        architecture_name = architecture_type.get("name", "")
        architecture_slug = architecture_type.get("slug", "")
        architecture_description = architecture_type.get("description", "") # có cũng được, không có không sao
        architecture_imageUrl = architecture_type.get("imageUrl", "")

        # kiểm tra xem có name không và có phải là string không
        if not architecture_name or not isinstance(architecture_name, str):
            logger.warning(f"Skipping record with missing name at index {idx}")
            continue

        # kiểm tra xem có imageUrl không và có phải là string không
        if not architecture_imageUrl or not isinstance(architecture_imageUrl, str):
            logger.warning(f"Skipping record with missing imageUrl at index {idx}")
            continue

        main_text = [
            f"Loại kiến trúc: {architecture_name}",
            f"Hình ảnh minh họa kiến trúc {architecture_name}: {architecture_imageUrl}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "architecture_type",
                "source": "architectureTypes.json",
                "architecture_id": architecture_id,
                "architecture_name": architecture_name,
                "architecture_slug": architecture_slug,
                "architecture_description": architecture_description,
                "architecture_image_url": architecture_imageUrl,
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid architecture types records found in {file_path}")

    return chunks