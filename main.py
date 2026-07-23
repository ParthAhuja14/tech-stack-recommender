"""
main.py
--------
Command-line entry point for the Tech Stack Recommender.

Usage:
    # Interactive mode
    python main.py

    # Non-interactive mode (comma-separated skills)
    python main.py --skills "Python,Cloud Computing,Automation" --top 3

    # Run the mini demo used in the project write-up
    python main.py --demo
"""

import argparse
import os

from src.recommender import TechStackRecommender

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "raw_skills.csv")


def print_recommendations(recommendations, user_skills):
    print("\n" + "=" * 60)
    print(f"Input Skills : {', '.join(user_skills)}")
    print("=" * 60)

    if not recommendations:
        print("No matches found.")
        return

    for rank, rec in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {rec.job_role}  —  {rec.match_percentage}% match")
        print(f"     Required Skills : {rec.required_skills}")
        print(f"     About           : {rec.description}")
    print("\n" + "=" * 60 + "\n")


def run_demo(engine: TechStackRecommender):
    demo_profiles = [
        ["Python", "Cloud Computing", "Automation"],
        ["JavaScript", "React", "HTML"],
        ["Networking", "Security", "Linux"],
    ]
    for skills in demo_profiles:
        recs = engine.recommend(skills, top_n=3)
        print_recommendations(recs, skills)


def main():
    parser = argparse.ArgumentParser(description="AI-Powered Tech Stack Recommender")
    parser.add_argument(
        "--skills", type=str, help="Comma-separated list of skills, e.g. 'Python,SQL,Docker'"
    )
    parser.add_argument("--top", type=int, default=3, help="Number of recommendations to return")
    parser.add_argument("--demo", action="store_true", help="Run a scripted demo with sample profiles")
    args = parser.parse_args()

    engine = TechStackRecommender(DATA_PATH)

    if args.demo:
        run_demo(engine)
        return

    if args.skills:
        user_skills = [s.strip() for s in args.skills.split(",")]
    else:
        print("Tech Stack Recommender — enter at least 3 skills separated by commas.")
        raw = input("Your skills: ")
        user_skills = [s.strip() for s in raw.split(",")]

    try:
        recommendations = engine.recommend(user_skills, top_n=args.top)
        print_recommendations(recommendations, user_skills)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
