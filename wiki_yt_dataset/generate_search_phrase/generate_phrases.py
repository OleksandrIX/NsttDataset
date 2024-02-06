import os
from loguru import logger
from .read_documents import read_random_documents
from .phrases_utils import filter_phrases
from .calculate_ngrams import calculate_ngrams


def write_output_phrases(file_name: str, ngrams: list, output_path: str) -> None:
    os.makedirs(output_path, exist_ok=True)
    language_code = os.path.basename(file_name).split("_")[0]
    output_file_name = f"{language_code}_search_phrases.txt"
    output_path_name = os.path.join(output_path, output_file_name)

    logger.info(f"Writing output to {output_path_name}")
    os.makedirs(os.path.dirname(output_path_name), exist_ok=True)
    with open(output_path_name, "w") as fout:
        for ngram in ngrams:
            fout.write(f"{ngram}\n")


def generate_phrases(filename: str,
                     output_path: str,
                     document_limit: int,
                     document_top_phrases: int,
                     phrase_length: int) -> None:
    documents = read_random_documents(filename, document_limit)

    ngrams = calculate_ngrams(documents, document_top_phrases, phrase_length)

    language_code = os.path.basename(filename).split('_')[0]
    valid_phrases = filter_phrases(ngrams, language_code)

    write_output_phrases(filename, valid_phrases, output_path)
