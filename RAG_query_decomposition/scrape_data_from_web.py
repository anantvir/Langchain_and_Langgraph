from dotenv import load_dotenv
import bs4
from langchain_community.document_loaders import WebBaseLoader
import os

load_dotenv()

def scrape_data_from_url(url):
    # Only keep post title, headers, and content from the full HTML.
    loader = WebBaseLoader(
    web_paths=(url,),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
    )
    docs = loader.load()

    return docs


