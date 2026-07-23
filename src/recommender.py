"""
recommender.py
----------------
Tech Stack Recommender — Content-Based Filtering Engine.

This module implements the "Digital Matchmaker" logic skeleton described in the
Project 3 brief: it maps a user's raw skills to the most relevant job roles /
tech stacks using TF-IDF feature weighting and Cosine Similarity, following the
Input -> Process -> Output (IPO) architecture.

Pipeline (as required by the assignment):
    1. Ingestion  -> capture user state (minimum 3 skills)
    2. Scoring    -> vectorize with TF-IDF and score with Cosine Similarity
    3. Sorting    -> rank items by descending similarity score
    4. Filtering  -> truncate to the Top-N most relevant matches

Author: DecodeLabs AI Internship — Project 3
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Recommendation:
    """A single ranked recommendation returned by the engine."""
    job_role: str
    match_score: float          # cosine similarity, 0.0 - 1.0
    match_percentage: float     # human-friendly percentage
    description: str
    required_skills: str


class TechStackRecommender:
    """
    Content-based recommendation engine that matches a user's skill profile
    against a catalog of job roles using TF-IDF weighted Cosine Similarity.
    """

    MIN_SKILLS_REQUIRED = 3

    def __init__(self, data_path: str):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at: {data_path}")

        self.df = pd.read_csv(data_path)
        self._validate_dataset()

        # Step 0: Normalize the skill vocabulary so multi-word skills
        # (e.g. "Machine Learning") are treated as a single token instead of
        # being split into "machine" and "learning". This keeps the vector
        # space consistent between items and user input (see slide:
        # "Bridging the Language Barrier Through Vector Mapping").
        self.df["skills_clean"] = self.df["required_skills"].apply(self._normalize_text)

        # Step 1 (partial - catalog side): Feature extraction with TF-IDF.
        # A custom token pattern ensures our underscore-joined skill tokens
        # (e.g. "machine_learning") are not broken apart by the default
        # regex, which only matches word characters of length >= 2.
        self.vectorizer = TfidfVectorizer(token_pattern=r"[^\s]+")
        self.item_matrix = self.vectorizer.fit_transform(self.df["skills_clean"])

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def recommend(self, user_skills: List[str], top_n: int = 3) -> List[Recommendation]:
        """
        Run the full 4-step ranking pipeline (Ingestion -> Scoring ->
        Sorting -> Filtering) and return the Top-N job role matches.

        Args:
            user_skills: list of raw skill strings provided by the user.
            top_n: number of top matches to return.

        Returns:
            A list of Recommendation objects sorted by descending match score.
        """
        # --- Step 1: Ingestion --------------------------------------------------
        clean_skills = self._ingest(user_skills)

        # --- Step 2: Scoring (Cosine Similarity over TF-IDF vectors) -----------
        scores = self._score(clean_skills)

        # --- Cold Start handling -------------------------------------------------
        if scores.max() == 0:
            return self._cold_start_fallback(top_n)

        # --- Step 3 & 4: Sorting + Filtering (Top-N) ----------------------------
        return self._sort_and_filter(scores, top_n)

    # ------------------------------------------------------------------ #
    # Pipeline steps
    # ------------------------------------------------------------------ #
    def _ingest(self, user_skills: List[str]) -> str:
        """Step 1: Capture and validate user state (minimum 3 skills)."""
        cleaned = [s.strip() for s in user_skills if s and s.strip()]

        if len(cleaned) < self.MIN_SKILLS_REQUIRED:
            raise ValueError(
                f"At least {self.MIN_SKILLS_REQUIRED} skills are required for "
                f"accurate matching. You provided {len(cleaned)}."
            )
        return self._normalize_text(", ".join(cleaned))

    def _score(self, user_text: str):
        """Step 2: Transform user text into the shared TF-IDF space and score."""
        user_vector = self.vectorizer.transform([user_text])
        similarity_scores = cosine_similarity(user_vector, self.item_matrix).flatten()
        return similarity_scores

    def _sort_and_filter(self, scores, top_n: int) -> List[Recommendation]:
        """Steps 3 & 4: Rank items by score, descending, and truncate to Top-N."""
        ranked_df = self.df.copy()
        ranked_df["match_score"] = scores
        ranked_df = ranked_df.sort_values(by="match_score", ascending=False)
        ranked_df = ranked_df[ranked_df["match_score"] > 0].head(top_n)

        return [
            Recommendation(
                job_role=row["job_role"],
                match_score=round(float(row["match_score"]), 4),
                match_percentage=round(float(row["match_score"]) * 100, 2),
                description=row["description"],
                required_skills=row["required_skills"],
            )
            for _, row in ranked_df.iterrows()
        ]

    def _cold_start_fallback(self, top_n: int) -> List[Recommendation]:
        """
        Handle the 'User Cold Start' problem: if a user's skills share no
        vocabulary overlap with the catalog, fall back to the most popular
        (trending) job roles instead of returning an empty result.
        """
        fallback_df = self.df.sort_values(by="popularity", ascending=False).head(top_n)
        return [
            Recommendation(
                job_role=row["job_role"],
                match_score=0.0,
                match_percentage=0.0,
                description=row["description"] + " (Trending fallback — no direct skill overlap found.)",
                required_skills=row["required_skills"],
            )
            for _, row in fallback_df.iterrows()
        ]

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normalize a comma-separated skills string into whitespace-separated
        underscore tokens so multi-word skills map to a single vocabulary
        dimension, e.g. "Machine Learning, SQL" -> "machine_learning sql".
        """
        tokens = [t.strip().lower().replace(" ", "_") for t in text.split(",")]
        return " ".join(t for t in tokens if t)

    def _validate_dataset(self) -> None:
        required_columns = {"job_role", "required_skills", "description", "popularity"}
        missing = required_columns - set(self.df.columns)
        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")
        if self.df.empty:
            raise ValueError("Dataset is empty.")
