# Tech Stack Recommender

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A command-line tool that recommends tech job roles based on your skill set.
Enter the skills you have, and the recommender matches them against a
dataset of job roles, returning the closest matches ranked by percentage
match — along with each role's required skills and a short description.

## Features

- **Interactive mode** — enter your skills at a prompt
- **Non-interactive mode** — pass skills directly as a CLI argument, ideal
  for scripting
- **Demo mode** — runs a scripted set of sample profiles (Python/Cloud/
  Automation, JavaScript/React/HTML, Networking/Security/Linux) to quickly
  showcase how the recommender behaves
- Configurable number of recommendations returned (`--top`)

## Requirements

- Python 3.8+
- No external dependencies beyond the standard library (adjust if
  `src/recommender.py` relies on packages like `pandas`; add those to
  `requirements.txt`)

## Project Structure

```
tech-stack-recommender/
├── main.py                  # CLI entry point
├── src/
│   └── recommender.py        # TechStackRecommender engine
├── data/
│   └── raw_skills.csv        # Skills / job-role dataset
├── README.md
├── requirements.txt
└── .gitignore
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/tech-stack-recommender.git
   cd tech-stack-recommender
   ```

2. (Optional) Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the recommender.

## Usage

**Interactive mode** — you'll be prompted to enter your skills:
```bash
python main.py
```

**Non-interactive mode** — pass a comma-separated list of skills and the
number of recommendations to return:
```bash
python main.py --skills "Python,Cloud Computing,Automation" --top 3
```

**Demo mode** — runs the sample profiles used in the project write-up:
```bash
python main.py --demo
```

### Example Output

```
============================================================
Input Skills : Python, Cloud Computing, Automation
============================================================

#1  DevOps Engineer  —  87% match
     Required Skills : Python, Cloud Computing, CI/CD, Automation
     About           : Builds and maintains deployment pipelines...

#2  Cloud Engineer  —  75% match
     Required Skills : Cloud Computing, Python, Networking
     About           : Designs and manages cloud infrastructure...
============================================================
```

## CLI Arguments

| Argument     | Description                                              | Default |
|--------------|-----------------------------------------------------------|---------|
| `--skills`   | Comma-separated list of skills, e.g. `"Python,SQL,Docker"` | —       |
| `--top`      | Number of recommendations to return                        | `3`     |
| `--demo`     | Run a scripted demo with sample profiles                   | `False` |

## Data

The recommender reads its skill/job-role dataset from `data/raw_skills.csv`.
To customize recommendations, update this file with your own job roles,
required skills, and descriptions.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull
request.

## License

This project is licensed under the MIT License. You're free to use, modify,
and distribute this software, provided the original copyright notice is
retained. See the [LICENSE](LICENSE) file for the full text.
