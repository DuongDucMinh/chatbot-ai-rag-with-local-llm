# Thu thập lại tất cả các chunk đã được tạo ra trong folder chunking và đẩy dữ liệu lên vector store
import logging

from core.setup_logging import setup_logging
from core.load_settings import load_settings

from vectorstore.upsert import upsert_chunks_to_vector_store # upsert chunk lên vector store
from chunking.architectureTypes import chunk_architecture_types
from chunking.companyInfo import chunk_company_info
from chunking.heroSlides import chunk_hero_slides
from chunking.interiorStyles import chunk_interior_styles
from chunking.news import chunk_news
from chunking.newsCategories import chunk_news_categories
from chunking.projectCategories import chunk_project_categories
from chunking.projects import chunk_projects

setting = load_settings()
setup_logging()
logger = logging.getLogger("ingestion")

def upload_chunks():
    all_chunks = []

    all_chunks.extend(chunk_architecture_types(setting))
    all_chunks.extend(chunk_company_info(setting))
    all_chunks.extend(chunk_hero_slides(setting))
    all_chunks.extend(chunk_interior_styles(setting))
    all_chunks.extend(chunk_news(setting))
    all_chunks.extend(chunk_news_categories(setting))
    all_chunks.extend(chunk_project_categories(setting))
    all_chunks.extend(chunk_projects(setting))

    logger.info(f"Total chunks to upload: {len(all_chunks)}")
    upsert_chunks_to_vector_store(all_chunks)
    logger.info("Finished uploading chunks to vector store")

if __name__ == "__main__":
    upload_chunks()