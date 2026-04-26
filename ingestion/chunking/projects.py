import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_projects(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "projects.json"

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
        logger.error(f"Error processing projects: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No projects found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"Projects data is not a list")
        return []
    
    chunks = []

    for idx, project in enumerate(data):
        if not isinstance(project, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        project_id = project.get("id")
        project_title = project.get("title", "")
        if not project_title or not isinstance(project_title, str):
            logger.warning(f"Skipping record with invalid projecttitle at index {idx}")
            continue

        project_slug = project.get("slug")
        project_description = project.get("description", "")
        project_investor = project.get("investor", "")
        project_location = project.get("location", "")
        project_area = project.get("area", "")
        project_completed_date = project.get("completedDate", "")
        project_view_count = project.get("viewCount", "")

        project_category = project.get("category", {}) # do đây là dự án nên loại dự án là quan trọng
        if not project_category or not isinstance(project_category, dict):
            logger.warning(f"Skipping record with invalid project category at index {idx}")
            continue
        
        project_category_id = project_category.get("id")
        project_category_name = project_category.get("name", "")
        if not project_category_name or not isinstance(project_category_name, str):
            logger.warning(f"Skipping record with invalid project category name at index {idx}")
            continue

        project_category_slug = project_category.get("slug")

        project_interior_style = project.get("interiorStyle", {}) # do đây là dự án nên phong cách nội thất cũng quan trọng
        if not project_interior_style or not isinstance(project_interior_style, dict):
            logger.warning(f"Skipping record with invalid interior style at index {idx}")
            continue

        project_interior_style_id = project_interior_style.get("id")
        project_interior_style_name = project_interior_style.get("name", "")
        project_interior_style_slug = project_interior_style.get("slug")

        project_architect = project.get("architect", {}) # do đây là dự án nên kiến trúc sư cũng quan trọng
        if not project_architect or not isinstance(project_architect, dict):
            logger.warning(f"Skipping record with invalid architect at index {idx}")
            continue

        project_architect_id = project_architect.get("id")
        project_architect_name = project_architect.get("name", "")
        if not project_architect_name or not isinstance(project_architect_name, str):
            logger.warning(f"Skipping record with invalid architect name at index {idx}")
            continue

        project_architect_slug = project_architect.get("slug")

        main_text = [
            f"Tên dự án: {project_title}",
            f"Slug dự án: {project_slug}",
            f"Mô tả dự án: {project_description}",
            f"Nhà đầu tư: {project_investor}",
            f"Địa điểm: {project_location}",
            f"Diện tích: {project_area}",
            f"Ngày hoàn thành: {project_completed_date}",
            f"Số lượt xem: {project_view_count}",
            f"Loại dự án: {project_category_name}",
            f"Phong cách nội thất: {project_interior_style_name}",
            f"Loại kiến trúc: {project_architect_name}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "project",
                "source": "projects.json",
                "project_id": project_id,
                "project_title": project_title,
                "project_slug": project_slug,
                "project_description": project_description,
                "project_investor": project_investor,
                "project_location": project_location,
                "project_area": project_area,
                "project_completed_date": project_completed_date,
                "project_view_count": project_view_count,
                "project_category": project_category,
                "project_category_id": project_category_id,
                "project_category_slug": project_category_slug,
                "project_interior_style": project_interior_style,
                "project_interior_style_id": project_interior_style_id,
                "project_interior_style_slug": project_interior_style_slug,
                "project_architect": project_architect,
                "project_architect_id": project_architect_id,
                "project_architect_slug": project_architect_slug
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid projects records found in {file_path}")

    return chunks