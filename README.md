# Reddit-Persona-Classification-Model-
Made a persona classification especially for reddit users enabling knowing about their interest, occupation, personality etc.
🧠Project Introduction

Reddit User Persona Analyzer is a Python-based project that leverages Natural Language Processing (NLP) and Large Language Models (LLMs) to generate insightful personality profiles of Reddit users. By analyzing a user's posts and comments, the system detects interests, tone, writing style, personality traits, occupation clues, and more.

The tool performs a two-level analysis:

    Basic NLP Layer: Uses keyword mapping and sentiment analysis (via TextBlob) to extract key personality and behavioral attributes.

    LLM-Based Analysis: Utilizes OpenAI’s GPT model to infer deeper, nuanced persona traits such as possible age group, profession, worldview, and more, with supporting textual evidence.

This project demonstrates how unstructured user-generated content from social media platforms can be transformed into structured behavioral insights — an important capability in fields like personalized marketing, digital psychology, and recommendation systems.

📂 Content Breakdown:
This repository contains the following key files and directories:
| File                    | Description                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `README.md`             | Project documentation including overview, setup, usage instructions, and technical details.                       |
| `reddituserpersona2.py` | Executable Python script that analyzes a Reddit user's posts/comments using NLP and generates a detailed persona. |
| `kojied_persona.txt`    | Sample output file containing the generated persona report for the Reddit user `u/kojied`.                        |

🛠 Tech Stack

This project leverages a combination of technologies and APIs to perform Reddit user analysis:
| Technology / Library                   | Purpose                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------- |
| **Python**                             | Core programming language used for scripting and logic.                 |
| **PRAW** (`Python Reddit API Wrapper`) | To fetch Reddit user posts and comments using the Reddit API.           |
| **TextBlob**                           | For basic NLP tasks such as sentiment analysis and tone classification. |
| **OpenAI GPT-4 API**                   | For advanced LLM-based persona generation based on user content.        |
| **Regex (re module)**                  | For extracting Reddit usernames from URLs.                              |
| **File I/O**                           | To save and format the generated persona reports.                       |


⚙️ Setup & Execution Instructions

Follow these steps to set up and run the project for any Reddit user profile:
1️⃣Install Required Libraries:
praw
textblob
openai
2️⃣Configure Reddit and OpenAI API Keys:
You can either edit them directly in the script (reddituserpersona2.py) or set them as environment variables.
Option A: Edit the Script Directly

Open reddituserpersona2.py and replace:

REDDIT_CLIENT_ID = "your-client-id"
REDDIT_CLIENT_SECRET = "your-client-secret"
REDDIT_USER_AGENT = "your-user-agent"
OPENAI_API_KEY = "your-openai-key"

3️⃣Run the Script

To analyze a Reddit user's profile, run:

python reddituserpersona2.py

📥 Enter the Reddit profile URL when prompted (e.g., https://www.reddit.com/user/kojied/).

✅ The script will:

    Scrape the user's submissions and comments.

    Perform NLP-based analysis.

    Call GPT-4 for deep persona insights.

    Save the output as (searched_user_name)_persona.txt.

🧩(Optional) Enable GPT-4 Based LLM Analysis

If you have access to GPT-4 via the OpenAI API, the script will automatically generate a deeper persona analysis using LLMs.

🧠 This includes:

    More nuanced traits like age, tone, writing style, ideology, etc.

    Evidence-backed characteristics using actual Reddit quotes

    ⚠️ Note: If you don't have GPT-4 access or have an invalid key, the script will gracefully fall back to basic NLP-based persona generation only.

To ensure LLM analysis works:

    Use a valid GPT-4 enabled API key

    Do not exceed the request or token limits
