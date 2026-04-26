import json
import logging
from pathlib import Path

from bs4 import BeautifulSoup

logger = logging.getLogger("ingestion")

# Lấy toàn bộ text trong HTML
def html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)
    # separator=" " chèn dấu " " giữa các đoạn text tránh dính chữ
    # strip=True để loại bỏ khoảng trắng thừa ở đầu và cuối văn bản

def chunk_news(setting):
    file_path = Path(setting["data"]["processed_dir"]) / "news.json"

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
        logger.error(f"Error processing news: {e}")
        return []
    
    # nếu trong bảng không có dữ liệu
    if not data:
        logger.warning(f"No news items found in {file_path}")
        return []
    
    if isinstance(data, dict):
        data = [data]  # Chuyển dict thành list nếu cần
    
    if not isinstance(data, list):
        logger.error(f"News data is not a list")
        return []
    
    chunks = []
    
    for idx, news_item in enumerate(data):
        if not isinstance(news_item, dict):
            logger.warning(f"Skipping non-dict record at index {idx}")
            continue
        
        news_title = news_item.get("title", "")
         # kiểm tra xem có title không và có phải là string không
        if not news_title or not isinstance(news_title, str):
            logger.warning(f"Skipping news item with invalid title at index {idx}")
            continue
    
        news_excerpt = news_item.get("excerpt", "")
         # kiểm tra xem có excerpt không và có phải là string không
        if not news_excerpt or not isinstance(news_excerpt, str):
            logger.warning(f"Skipping news item with invalid excerpt at index {idx}")
            continue

        news_content = news_item.get("content", "")
        if not news_content or not isinstance(news_content, str):
            logger.warning(f"Skipping news item with invalid content at index {idx}")
            continue
        news_content_text = html_to_text(news_content) # chuyển HTML thành text thuần

        news_thumbnail_url = news_item.get("thumbnailUrl") # có thể có hoặc không nên không cần kiểm tra kiểu dữ liệu
        news_category = news_item.get("category", {}) # đối với tin tức thì category không phải là thông tin quá quan trọng
        news_category_id = news_category.get("id") 
        news_category_name = news_category.get("name") 
        news_category_slug = news_category.get("slug")

        main_text = [
            f"Tiêu đề tin tức: {news_title}",
            f"Tóm tắt tin tức: {news_excerpt}",
            f"Nội dung chi tiết: {news_content_text}",
        ]

        chunks.append({
            "text": "\n".join(main_text),
            "metadata": {
                "type": "news",
                "source": "news.json",
                "title": news_title,
                "excerpt": news_excerpt,
                "content": news_content_text,
                "thumbnail_url": news_thumbnail_url,
                "category": news_category,
                "category_id": news_category_id,
                "category_name": news_category_name, 
                "category_slug": news_category_slug
            }
        })

    if not chunks:
        logger.warning(f"No valid news items found in {file_path}")
    
    return chunks