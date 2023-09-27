import os

from dotenv import load_dotenv

import document_scraper
from document_scraper import DataLoader
from document_scraper import SourceType
from opencopilot import OpenCopilot

load_dotenv()

data_dir = "data"
data_loaders = [
    DataLoader(
        source_type=SourceType.GITBOOK,
        sources=[
            "https://docs.readyplayer.me/ready-player-me/"
        ],
        destination_file=f"{data_dir}/serialized_documents_rpm_gitbook.json"
    ),
    DataLoader(
        source_type=SourceType.URL,
        sources=[
            "https://docs.readyplayer.me/asset-creation-guide/asset-creation/overview",
            "https://readyplayer.me/company/about-us",
            "https://readyplayer.me/developers",
            "https://readyplayer.me/brands-creators",
            "https://readyplayer.me/case-studies/adidas-originals-uses-ai-to-create-10-million-personal-avatars",
            "https://readyplayer.me/case-studies/bmws-immersive-experiences-with-3d-avatars",
            "https://readyplayer.me/case-studies/look-great-anywhere-with-tommy-hilfiger-parallel-collection",
        ],
        destination_file=f"{data_dir}/serialized_documents_rpm_pages.json"
    ),
    DataLoader(
        source_type=SourceType.BLOG,
        sources=[
            "https://readyplayer.me/blog-categories/for-developers",
            "https://readyplayer.me/blog-categories/changelog"
        ],
        destination_file=f"{data_dir}/serialized_documents_rpm_blog.json"
    )
]
document_scraper.execute(data_loaders=data_loaders)

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name="rpm",
    auth_type=None,
    helicone_api_key=os.getenv("HELICONE_API_KEY")
)
copilot.add_local_files_dir("data")

copilot()
