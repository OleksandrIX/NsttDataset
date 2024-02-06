import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from loguru import logger


def calculate_ngrams(documents: list, document_top_phrases: int, phrase_length: int) -> list:
    logger.info("Generating search phrases")

    tfidf_vectorized = TfidfVectorizer(
        ngram_range=(phrase_length, phrase_length),
        use_idf=True
    )

    tfidf_vectorized_vectors = tfidf_vectorized.fit_transform(documents)
    feature_names = np.array(tfidf_vectorized.get_feature_names_out())

    ngrams = feature_names[
        np.argsort(-tfidf_vectorized_vectors.toarray(), axis=1)[:, :document_top_phrases]
    ].flatten().tolist()

    return ngrams
