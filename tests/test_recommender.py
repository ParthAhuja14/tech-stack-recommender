"""
test_recommender.py
---------------------
Unit tests for the TechStackRecommender engine.

Run with:
    pytest -v
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import TechStackRecommender

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_skills.csv")


@pytest.fixture(scope="module")
def engine():
    return TechStackRecommender(DATA_PATH)


def test_dataset_loads_correctly(engine):
    assert not engine.df.empty
    assert "job_role" in engine.df.columns


def test_minimum_skill_validation(engine):
    with pytest.raises(ValueError):
        engine.recommend(["Python", "SQL"])  # only 2 skills, should fail


def test_recommend_returns_top_n(engine):
    results = engine.recommend(["Python", "SQL", "Machine Learning"], top_n=3)
    assert len(results) <= 3
    assert len(results) > 0


def test_recommend_scores_are_sorted_descending(engine):
    results = engine.recommend(["Python", "SQL", "Machine Learning", "Statistics"], top_n=5)
    scores = [r.match_score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_relevant_profile_matches_expected_role(engine):
    results = engine.recommend(["AWS", "Docker", "Kubernetes", "CI/CD"], top_n=1)
    assert results[0].job_role == "DevOps Engineer"


def test_cold_start_returns_fallback_trending_roles(engine):
    # Skills with zero vocabulary overlap with the catalog
    results = engine.recommend(["Zzznonexistent", "Skillxyz", "Randomtag"], top_n=3)
    assert len(results) == 3
    assert all(r.match_score == 0.0 for r in results)


def test_match_percentage_within_valid_range(engine):
    results = engine.recommend(["Python", "SQL", "Data Analysis"], top_n=3)
    for r in results:
        assert 0.0 <= r.match_percentage <= 100.0
