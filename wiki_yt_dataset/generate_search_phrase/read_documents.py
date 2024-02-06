import json
import random
from tqdm import tqdm
from loguru import logger


def read_random_documents(filename: str, documents_count: int) -> list:
    documents = []

    logger.info(f"Selecting {documents_count} random documents")
    with open(filename, encoding="utf-8") as file:
        all_documents = [json.loads(line) for line in file]
    selected_documents = random.sample(all_documents, min(documents_count, len(all_documents)))

    progress_bar = tqdm(selected_documents)
    progress_bar.set_description("Processing random documents")

    for document in progress_bar:
        documents.append(document["title"] + "\n" + document["text"])

    return documents
