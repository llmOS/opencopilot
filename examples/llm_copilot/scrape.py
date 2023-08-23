import document_scraper
from document_scraper import DataLoader
from document_scraper import SourceType

DATA_LOADERS = [
    DataLoader(
        source_type=SourceType.OPENAI_DOCS,
        sources=[
            "https://platform.openai.com/docs/"
        ],
        destination_file="data/serialized_documents_openai_docs.json"
    ),
    DataLoader(
        source_type=SourceType.OPENAI_API_DOCS,
        sources=[
            "https://platform.openai.com/docs/api-reference",
        ],
        destination_file="data/serialized_documents_openai_api_docs.json"
    ),
    DataLoader(
        source_type=SourceType.ANTHROPIC_DOCS,
        sources=[
            "https://docs.anthropic.com/claude/docs",
            "https://docs.anthropic.com/claude/reference/",
        ],
        destination_file="data/serialized_documents_anthropic.json"
    ),
    DataLoader(
        source_type=SourceType.URL,
        sources=[
            "https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/",
            "https://www.sequoiacap.com/article/llm-stack-perspective/",
            "https://huyenchip.com/2023/04/11/llm-engineering.html",
        ],
        destination_file="data/serialized_documents_blogs.json"
    ),
    DataLoader(
        source_type=SourceType.PROMPTING_GUIDE_DOCS,
        sources=[
            "https://www.promptingguide.ai/",
        ],
        destination_file="data/serialized_documents_prompting_guide_docs.json"
    ),
    DataLoader(
        source_type=SourceType.FULLSTACK_DEEPLEARNING,
        sources=[
            "https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/",
        ],
        destination_file="data/serialized_documents_fullstack_deeplearning.json"
    )
]

if __name__ == "__main__":
    document_scraper.execute(data_loaders=DATA_LOADERS)
