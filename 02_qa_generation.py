
import os
import json
from dotenv import load_dotenv  

from doc_loader.pdfLoader import load_pdf_files
from ingest_data.acs_ingest import generate_qna

load_dotenv()  

service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")  
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")  
key = os.getenv("AZURE_SEARCH_ADMIN_KEY")

with open('search_config.json', 'r') as json_file:
    data = json.load(json_file)

chunk_sizes = data["chunking"]["chunk_size"]
overall_size = data["chunking"]["overall_size"]

embedding_dimensions = data["embedding_dimension"]
efConstructions = data["efConstruction"]
efsearchs = data["efsearch"]
name_prefix = data["name_prefix"]

all_docs = load_pdf_files("./data/", 2000, 0)
generate_qna(all_docs)