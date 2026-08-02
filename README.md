# 🧭 Tech Stack Recommender — Intelligent Career Role Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-Command%20Line-success)
[![CI](https://github.com/ParthAhuja14/tech-stack-recommender/actions/workflows/ci.yml/badge.svg)](https://github.com/ParthAhuja14/tech-stack-recommender/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> A Python-based recommendation engine that analyzes a user's technical skills and recommends the most suitable software engineering roles using a transparent skill-matching algorithm. Designed as a lightweight, explainable career recommendation system.

---

# 📖 Table of Contents

- Overview
- Problem Statement
- Architecture
- Project Structure
- Installation
- Usage
- Example Output
- Recommendation Methodology
- CLI Arguments
- Testing
- Tech Stack
- Future Improvements
- License

---

# 📌 Overview

Choosing the right software engineering career path can be difficult when multiple roles share overlapping skills.

This project simulates an intelligent career recommendation engine. Instead of relying on hard-coded career suggestions, it compares a user's skills against a dataset of job roles, calculates a percentage match for each role, ranks the results, and explains why each recommendation was made.

The application supports interactive mode, command-line arguments, and a demonstration mode for quickly showcasing the recommendation engine.

---

# 🎯 Problem Statement

Design a lightweight recommendation engine that:

- Accepts a user's technical skills
- Compares them with predefined job-role requirements
- Calculates a matching score
- Returns the most suitable career paths ranked by relevance

---

# 🏗 Architecture

```text
User Skills
      │
      ▼
Input Validation
      │
      ▼
Skill Normalization
      │
      ▼
Load Job Dataset
      │
      ▼
Skill Matching Engine
      │
      ▼
Percentage Match Calculation
      │
      ▼
Ranking (Top-K)
      │
      ▼
Formatted CLI Output
```

---

# 🗂 Project Structure

```text
tech-stack-recommender/
├── data/
│   └── raw_skills.csv
├── src/
│   └── recommender.py
├── tests/
│   └── test_recommender.py
├── .github/workflows/ci.yml
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

# 💻 Installation

```bash
git clone https://github.com/ParthAhuja14/tech-stack-recommender.git
cd tech-stack-recommender

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

# 🚀 Usage

Interactive mode

```bash
python main.py
```

CLI mode

```bash
python main.py --skills "Python,Docker,AWS" --top 3
```

Demo mode

```bash
python main.py --demo
```

---

# 📊 Example Output

```text
Input Skills:
Python, Cloud Computing, Automation

1. DevOps Engineer
Match: 87%

Required Skills:
Python
Cloud Computing
CI/CD
Automation

Description:
Builds and maintains deployment pipelines.
```

---

# 🧠 Recommendation Methodology

Each job role is represented as a collection of required skills.

The recommendation score is computed as:

```text
Match % =
(Matching Skills ÷ Required Skills) × 100
```

The engine:

1. Loads the dataset.
2. Normalizes user input.
3. Compares every role.
4. Calculates percentage overlap.
5. Sorts results.
6. Returns the Top-K recommendations.

This transparent approach makes every recommendation explainable rather than a black-box prediction.

---

# ⚙ CLI Arguments

| Argument | Description |
|----------|-------------|
| `--skills` | Comma-separated list of skills |
| `--top` | Number of recommendations |
| `--demo` | Run predefined demonstrations |

---

# 🧪 Testing

Run unit tests locally:

```bash
python -m unittest discover tests -v
```

Tests validate:

- Recommendation scoring
- Ranking logic
- Input handling
- Result formatting

Every push and pull request against `main` runs this suite automatically via
GitHub Actions on Python 3.8 and 3.11 (see `.github/workflows/ci.yml`), so the
CI badge above reflects real, current test results rather than a static claim.

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.8+ |
| Interface | Command Line |
| Dataset | CSV |
| Testing | unittest |
| Dependencies | Python Standard Library |

---

# 🔮 Future Improvements

- Semantic skill matching using Sentence Transformers
- Resume parsing
- Skill-gap analysis
- Learning roadmap generation
- FastAPI backend
- Streamlit web interface
- LLM-powered career recommendations
- Recommendation explanations using AI

---

# 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
