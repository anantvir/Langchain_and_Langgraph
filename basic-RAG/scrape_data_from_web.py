from dotenv import load_dotenv
import bs4
from langchain_community.document_loaders import WebBaseLoader
import os

load_dotenv()

def scrape_data_from_url(url):
    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    return docs


