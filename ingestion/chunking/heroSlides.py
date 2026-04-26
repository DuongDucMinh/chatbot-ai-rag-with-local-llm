import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_hero_slides(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "heroSlides.json"

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
        logger.error(f"Error processing hero slides: {e}")
        return []
    
    if not data:
        logger.warning(f"No hero slides found in {file_path}")
        return []

    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần

    if not isinstance(data, list):
        logger.error(f"Hero slides data is not a list")
        return []

    chunks = []

    for idx, hero_slide in enumerate(data):
        if not isinstance(hero_slide, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue

        company_title = hero_slide.get("title", "")
        if not company_title or not isinstance(company_title, str):
            logger.warning(f"Skipping record with invalid title at index {idx}")
            continue

        company_subtitle = hero_slide.get("subtitle", "")
        if not company_subtitle or not isinstance(company_subtitle, str):
            logger.warning(f"Skipping record with invalid subtitle at index {idx}")
            continue

        company_description = hero_slide.get("description", "")
        if not company_description or not isinstance(company_description, str):
            logger.warning(f"Skipping record with invalid description at index {idx}")
            continue

        companny_image_url = hero_slide.get("imageUrl") # có thể có hoặc không nên không cần kiểm tra kiểu dữ liệu

        main_text = [
            f"Tiêu đề mục: {company_title}",
            f"Phụ đề mục cho {company_title}: {company_subtitle}",
            f"Mô tả chi tiết cho mục {company_title}: {company_description}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "hero_slide",
                "source": "heroSlides.json",
                "title": company_title,
                "subtitle": company_subtitle,
                "description": company_description,
                "image_url": companny_image_url
            }
        })

    if not chunks:
        logger.warning(f"No valid hero slides found in {file_path}")

    return chunks