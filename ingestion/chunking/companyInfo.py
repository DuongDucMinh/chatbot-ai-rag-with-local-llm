import json
import logging
from pathlib import Path

logger = logging.getLogger("ingestion")

def chunk_company_info(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "companyInfo.json" # str -> Path

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
        logger.error(f"Error processing company info: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No company info found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"Company info data is not a list")
        return []
    
    chunks = []

    for idx, company_info in enumerate(data):
        if not isinstance(company_info, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        company_name = company_info.get("companyName", "")
        # kiểm tra xem có name không và có phải là string không
        if not company_name or not isinstance(company_name, str):
            logger.warning(f"Skipping record with invalid name at index {idx}")
            continue
        
        company_slogan = company_info.get("companySlogan", "")
        if not company_slogan or not isinstance(company_slogan, str):
            logger.warning(f"Skipping record with invalid slogan at index {idx}")
            continue
    
        company_description = company_info.get("companyDescription", "")
        if not company_description or not isinstance(company_description, str):
            logger.warning(f"Skipping record with invalid description at index {idx}")
            continue
        
        company_hotlines = company_info.get("hotlines", [])  
        if not isinstance(company_hotlines, list):
            logger.warning(f"Skipping record with invalid hotlines at index {idx}")
            continue

        company_email = company_info.get("email", [])
        if not isinstance(company_email, list):
            logger.warning(f"Skipping record with invalid email at index {idx}")
            continue

        company_main_address = company_info.get("mainAddress", "")
        if not isinstance(company_main_address, str):
            logger.warning(f"Skipping record with invalid main address at index {idx}")
            continue

        company_working_hours = company_info.get("workingHours", "")
        if not company_working_hours or not isinstance(company_working_hours, str):
            logger.warning(f"Skipping record with invalid working hours at index {idx}")
            continue
    
        company_website = company_info.get("website", "")
        if not company_website or not isinstance(company_website, str):
            logger.warning(f"Skipping record with invalid website at index {idx}")
            continue

        company_social_links = company_info.get("socialLinks", {})
        # chỉ lấy những link tồn tại (khác null)
        if isinstance(company_social_links, dict):  
            company_social_text = ", ".join([f"{key}: {value}" for key, value in company_social_links.items() if value])

        company_total_employees = company_info.get("totalEmployees")
        if not isinstance(company_total_employees, int):
            logger.warning(f"Skipping record with invalid totalEmployees at index {idx}")
            continue 

        company_total_projects = company_info.get("totalProjects")
        if not isinstance(company_total_projects, int):
            logger.warning(f"Skipping record with invalid totalProjects at index {idx}")
            continue

        main_text = [
            f"Tên công ty: {company_name}",
            f"Khẩu hiệu công ty: {company_slogan}",
            f"Mô tả công ty: {company_description}",
            f"Hotlines: {', '.join(company_hotlines)}",
            f"Email: {', '.join(company_email)}",
            f"Địa chỉ chính: {company_main_address}",
            f"Giờ làm việc: {company_working_hours}",
            f"Website: {company_website}",
            f"Mạng xã hội: {company_social_text}",
            f"Tổng số nhân viên: {company_total_employees}",
            f"Tổng số dự án đã thực hiện: {company_total_projects}"
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "company_info",  # quan trọng nhất để biết loại chunk là gì
                "source": "companyInfo.json",
                "company_name": company_name,
                "company_slogan": company_slogan,
                "company_description": company_description,
                "company_hotlines": company_hotlines,
                "company_email": company_email,
                "company_main_address": company_main_address,
                "company_working_hours": company_working_hours,
                "company_website": company_website,
                "company_social_links": company_social_links,
                "company_total_employees": company_total_employees,
                "company_total_projects": company_total_projects
            }
        })

    # nếu không có chunks (record) nào thì đưa ra cảnh báo
    if not chunks:
        logger.warning(f"No valid company info records found in {file_path}")

    return chunks




















