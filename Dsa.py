import requests
import random
from datetime import datetime
import os

# 1. Fetch problem list
list_url = "https://leetcode.com/api/problems/all/"
res = requests.get(list_url)
data = res.json()
problems = data["stat_status_pairs"]

# 2. Pick a random problem
problem = random.choice(problems)
title = problem["stat"]["question__title"]
slug = problem["stat"]["question__title_slug"]
difficulty = {1: "Easy", 2: "Medium", 3: "Hard"}[problem["difficulty"]["level"]]

# 3. Fetch full description using GraphQL
graphql_url = "https://leetcode.com/graphql"
query = {
    "operationName": "getQuestionDetail",
    "variables": {"titleSlug": slug},
    "query": """query getQuestionDetail($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
            content
            difficulty
            topicTags { name slug }
        }
    }"""
}

res = requests.post(graphql_url, json=query)
question_data = res.json()["data"]["question"]

description_html = question_data["content"]

# Convert HTML to Markdown-ish text (simple cleanup)
from bs4 import BeautifulSoup
soup = BeautifulSoup(description_html, "html.parser")
description_text = soup.get_text("\n")

# 4. Save problem into a file
today = datetime.now().strftime("%Y-%m-%d")
os.makedirs("problems", exist_ok=True)
filename = f"problems/{today}.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# {title}\n")
    f.write(f"- Difficulty: {difficulty}\n")
    f.write(f"- Link: https://leetcode.com/problems/{slug}/\n\n")
    f.write("## Problem Statement\n\n")
    f.write(description_text.strip() + "\n\n")
    f.write("## My Solution\n\n```python\n# Write your solution here\n```\n")

print(f"Saved problem: {title}")
