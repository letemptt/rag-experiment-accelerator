
import os
import json
from dotenv import load_dotenv  
from init_Index.create_index import create_acs_index
from doc_loader.pdfLoader import load_pdf_files
from embedding.gen_embeddings import generate_embedding
from ingest_data.acs_ingest import upload_data, generate_qna
from nlp.preprocess import Preprocess

load_dotenv()  
pre_process = Preprocess()

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

all_index_config = "generated_index_names"

index_dict = {}
index_dict["indexes"] = []

for config_item in chunk_sizes:
    for overlap in overall_size:
        for dimension in embedding_dimensions:
            for efConstruction in efConstructions:
                for efsearch in efsearchs:
                    index_name = f"{name_prefix}-{config_item}-{overlap}-{dimension}-{efConstruction}-{efsearch}"
                    print(f"{name_prefix}-{config_item}-{overlap}-{dimension}-{efConstruction}-{efsearch}")
                    create_acs_index(service_endpoint,index_name, key, dimension, efConstruction, efsearch)
                    index_dict["indexes"].append(index_name) 
                    
with open(all_index_config, 'w') as index_name:
    json.dump(index_dict, index_name, indent=4)


for config_item in chunk_sizes:
    for overlap in overall_size:
        for dimension in embedding_dimensions:
            for efConstruction in efConstructions:
                for efsearch in efsearchs:
                    index_name = f"{name_prefix}-{config_item}-{overlap}-{dimension}-{efConstruction}-{efsearch}"
                    all_docs = load_pdf_files("./data/", config_item, overlap)
                    data_load = []
                    for docs in all_docs:
                        chunk_dict = {}
                        chunk_dict["content"] = docs.page_content
                        chunk_dict["content_vector"] = generate_embedding(dimension, str(Preprocess(docs.page_content)))
                        data_load.append(chunk_dict)
                    upload_data(data_load,service_endpoint,index_name,key, dimension)


    





