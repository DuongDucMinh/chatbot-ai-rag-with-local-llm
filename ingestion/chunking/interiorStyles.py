# chunking interior styles data thành nhiều chunk nhỏ (mỗi chunk là 1 record trong table interiorStyles)

import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_interior_styles(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "interiorStyles.json"

    # Nếu đường dẫn file không tồn tại
    if not file_path.exists():
        logger.error(f"Input file not found: {file_path}")
        return []   

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Successfully loaded data from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {file_path}: {e}") # nếu file json bị lỗi định dạng thì sẽ log lỗi 
        return []
    except Exception as e:
        logger.error(f"Error processing interior styles: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No interior styles found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"Interior styles data is not a list")
        return []
    
    chunks = []

    for idx, interior_style in enumerate(data):
        if not isinstance(interior_style, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        interior_style_id = interior_style.get("id")
        interior_style_name = interior_style.get("name", "")
        interior_style_slug = interior_style.get("slug")
        interior_style_description = interior_style.get("description") # có cũng được, không có không sao
        interior_style_imageUrl = interior_style.get("imageUrl", "")

        # kiểm tra xem có name không và có phải là string không
        if not interior_style_name or not isinstance(interior_style_name, str):
            logger.warning(f"Skipping record with missing name at index {idx}")
            continue

        # kiểm tra xem có imageUrl không và có phải là string không
        if not interior_style_imageUrl or not isinstance(interior_style_imageUrl, str):
            logger.warning(f"Skipping record with missing imageUrl at index {idx}")
            continue

        main_text = [
            f"Loại nội thất: {interior_style_name}",
            f"Hình ảnh minh họa nội thất {interior_style_name}: {interior_style_imageUrl}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "interior_style",
                "source": "interiorStyles.json",
                "interior_style_id": interior_style_id,
                "interior_style_name": interior_style_name,
                "interior_style_slug": interior_style_slug,
                "interior_style_description": interior_style_description,
                "interior_style_image_url": interior_style_imageUrl,
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid interior styles records found in {file_path}")

    return chunks