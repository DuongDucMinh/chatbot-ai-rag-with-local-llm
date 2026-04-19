import yaml
import os

def load_settings():
    with open("config/settings.yaml", "r", encoding="utf-8") as file:
        settings = yaml.safe_load(file)
    
    # Override với environment variable
    if os.getenv("APP_ENV"):
        settings["app"]["env"] = os.getenv("APP_ENV")

    # Vector database override
    if os.getenv("QDRANT_URL"):
        settings["vector_database"]["url"] = os.getenv("QDRANT_URL")
    if os.getenv("QDRANT_API_KEY"):
        settings["vector_database"]["api_key"] = os.getenv("QDRANT_API_KEY")
    if os.getenv("QDRANT_COLLECTION_NAME"):
        settings["vector_database"]["collection_name"] = os.getenv("QDRANT_COLLECTION_NAME")
    if os.getenv("QDRANT_TIMEOUT"):
        settings["vector_database"]["timeout"] = int(os.getenv("QDRANT_TIMEOUT"))

    # Embedding override
    if os.getenv("EMBEDDING_MODEL"):
        settings["embedding"]["model"] = os.getenv("EMBEDDING_MODEL")
    if os.getenv("EMBEDDING_DEVICE"):
        settings["embedding"]["device"] = os.getenv("EMBEDDING_DEVICE")
    if os.getenv("EMBEDDING_BATCH_SIZE"):
        settings["embedding"]["batch_size"] = int(os.getenv("EMBEDDING_BATCH_SIZE"))
    
    # LLM override
    if os.getenv("LLM_MODEL_NAME"):
        settings["llm"]["model"] = os.getenv("LLM_MODEL_NAME")
    if os.getenv("LLM_BASE_URL"):
        settings["llm"]["base_url"] = os.getenv("LLM_BASE_URL")
    if os.getenv("LLM_PROVIDER"):
        settings["llm"]["provider"] = os.getenv("LLM_PROVIDER")
    if os.getenv("LLM_TEMPERATURE"):
        settings["llm"]["temperature"] = float(os.getenv("LLM_TEMPERATURE"))
    if os.getenv("LLM_MAX_TOKENS"):
        settings["llm"]["max_tokens"] = int(os.getenv("LLM_MAX_TOKENS"))

    # Retrieval override
    if os.getenv("RETRIEVAL_TOP_K"):
        settings["retrieval"]["top_k"] = int(os.getenv("RETRIEVAL_TOP_K"))
    if os.getenv("RETRIEVAL_SCORE_THRESHOLD"):
        settings["retrieval"]["score_threshold"] = float(os.getenv("RETRIEVAL_SCORE_THRESHOLD"))
    if os.getenv("DENSE_WEIGHT"):
        settings["retrieval"]["dense_weight"] = float(os.getenv("DENSE_WEIGHT"))
    if os.getenv("BM25_WEIGHT"):
        settings["retrieval"]["sparse_weight"] = float(os.getenv("BM25_WEIGHT"))

    # Reranking override
    if os.getenv("RERANKING_MODEL"):
        settings["reranking"]["model"] = os.getenv("RERANKING_MODEL")
    if os.getenv("RERANKING_DEVICE"):
        settings["reranking"]["device"] = os.getenv("RERANKING_DEVICE")
    if os.getenv("RERANKING_TOP_K"):
        settings["reranking"]["top_k"] = int(os.getenv("RERANKING_TOP_K")) 

    return settings