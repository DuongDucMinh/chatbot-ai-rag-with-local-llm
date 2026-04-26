import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_news_categories(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "newsCategories.json"

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
        logger.error(f"Error processing news categories: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No news categories found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"News categories data is not a list")
        return []
    
    chunks = []

    for idx, news_category in enumerate(data):
        if not isinstance(news_category, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        news_category_id = news_category.get("id")
        news_category_name = news_category.get("name", "")
        news_category_slug = news_category.get("slug")
        news_category_description = news_category.get("description")

        # kiểm tra xem có name không và có phải là string không
        if not news_category_name or not isinstance(news_category_name, str):
            logger.warning(f"Skipping record with missing name at index {idx}")
            continue

        main_text = [
            f"Loại tin tức: {news_category_name}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "news_category",
                "source": "newsCategories.json",
                "news_category_id": news_category_id,
                "news_category_name": news_category_name,
                "news_category_slug": news_category_slug,
                "news_category_description": news_category_description
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid news categories records found in {file_path}")

    return chunks