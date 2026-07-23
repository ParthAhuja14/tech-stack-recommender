"""
manual_similarity.py
---------------------
A from-scratch (no scikit-learn) implementation of TF-IDF weighting and
Cosine Similarity, built to demonstrate a first-principles understanding of
the "pure similarity logic" referenced in the Project 3 brief — before
relying on scikit-learn's optimized vectorized implementation in
`recommender.py`.

This is intentionally kept simple and readable over performant; it mirrors
the exact math described in the project material:

    TF(t, d)  = (count of term t in document d) / (total terms in d)
    IDF(t)    = log(total documents / documents containing t)
    weight    = TF * IDF

    cosine_similarity(A, B) = (A . B) / (||A|| * ||B||)
"""

import math
from collections import Counter
from typing import Dict, List


def tokenize(skills_text: str) -> List[str]:
    """Turn a comma-separated skills string into normalized tokens."""
    return [
        skill.strip().lower().replace(" ", "_")
        for skill in skills_text.split(",")
        if skill.strip()
    ]


def compute_tf(tokens: List[str]) -> Dict[str, float]:
    """Term Frequency: how often a token appears within a single document."""
    counts = Counter(tokens)
    total_terms = len(tokens)
    return {term: count / total_terms for term, count in counts.items()}


def compute_idf(documents: List[List[str]]) -> Dict[str, float]:
    """Inverse Document Frequency: penalizes terms common across all documents."""
    num_docs = len(documents)
    df_counts: Counter = Counter()
    for doc in documents:
        for term in set(doc):
            df_counts[term] += 1

    return {
        term: math.log(num_docs / doc_freq)
        for term, doc_freq in df_counts.items()
    }


def compute_tfidf_vector(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    """Combine TF and IDF into a single weighted vector for one document."""
    tf = compute_tf(tokens)
    return {term: tf_val * idf.get(term, 0.0) for term, tf_val in tf.items()}


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """
    Cosine similarity between two sparse vectors represented as dicts:
    the angle between them, invariant to their magnitude.
    """
    shared_terms = set(vec_a.keys()) & set(vec_b.keys())
    dot_product = sum(vec_a[t] * vec_b[t] for t in shared_terms)

    magnitude_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    magnitude_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def rank_items(user_skills_text: str, item_documents: Dict[str, str], top_n: int = 3):
    """
    End-to-end demonstration of the manual pipeline:
    tokenize -> TF-IDF -> cosine similarity -> sort -> filter (Top-N).

    Args:
        user_skills_text: comma-separated skills, e.g. "Python, SQL, Docker"
        item_documents: dict mapping item name -> comma-separated skills string
        top_n: number of results to return
    """
    all_tokenized = [tokenize(text) for text in item_documents.values()] + [tokenize(user_skills_text)]
    idf = compute_idf(all_tokenized)

    item_vectors = {
        name: compute_tfidf_vector(tokenize(text), idf)
        for name, text in item_documents.items()
    }
    user_vector = compute_tfidf_vector(tokenize(user_skills_text), idf)

    scored = [
        (name, cosine_similarity(user_vector, vec))
        for name, vec in item_vectors.items()
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_n]


if __name__ == "__main__":
    # Small standalone demo — run with: python src/manual_similarity.py
    sample_items = {
        "Data Scientist": "Python, SQL, Machine Learning, Statistics",
        "DevOps Engineer": "AWS, Docker, Kubernetes, Automation",
        "Backend Developer": "Java, Python, SQL, APIs",
    }
    results = rank_items("Python, Cloud Computing, Automation", sample_items, top_n=3)
    print("Manual TF-IDF + Cosine Similarity demo:")
    for role, score in results:
        print(f"  {role:20s} -> {score:.4f}")
