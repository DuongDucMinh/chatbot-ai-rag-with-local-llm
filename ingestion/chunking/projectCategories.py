import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_project_categories(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "projectCategories.json"

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
        logger.error(f"Error processing project categories: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No project categories found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"Project categories data is not a list")
        return []
    
    chunks = []

    for idx, project_category in enumerate(data):
        if not isinstance(project_category, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        project_category_id = project_category.get("id")
        project_category_name = project_category.get("name", "")
        project_category_slug = project_category.get("slug")
        project_category_description = project_category.get("description")

        # kiểm tra xem có name không và có phải là string không
        if not project_category_name or not isinstance(project_category_name, str):
            logger.warning(f"Skipping record with missing name at index {idx}")
            continue

        main_text = [
            f"Loại dự án: {project_category_name}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "project_category",
                "source": "projectCategories.json",
                "project_category_id": project_category_id,
                "project_category_name": project_category_name,
                "project_category_slug": project_category_slug,
                "project_category_description": project_category_description
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid project categories records found in {file_path}")

    return chunks