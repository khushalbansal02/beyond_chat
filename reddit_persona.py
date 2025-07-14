import os
import praw
from dotenv import load_dotenv
import ollama

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

missing = []
if not REDDIT_CLIENT_ID:
    missing.append('REDDIT_CLIENT_ID')
if not REDDIT_CLIENT_SECRET:
    missing.append('REDDIT_CLIENT_SECRET')
if not REDDIT_USER_AGENT:
    missing.append('REDDIT_USER_AGENT')
if missing:
    raise EnvironmentError(f"Missing the following environment variables in your .env file: {', '.join(missing)}")

profile_url = input('Enter the Reddit user profile URL: ').strip()

def extract_username(url):
    if '/user/' in url:
        return url.split('/user/')[1].strip('/').split('/')[0]
    raise ValueError('Invalid Reddit profile URL')

username = extract_username(profile_url)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_user_content(username, limit=10):
    user = reddit.redditor(username)
    posts = []
    comments = []
    try:
        for submission in user.submissions.new(limit=limit):
            posts.append({
                'type': 'post',
                'title': submission.title,
                'body': submission.selftext,
                'permalink': f'https://reddit.com{submission.permalink}'
            })
        for comment in user.comments.new(limit=limit):
            comments.append({
                'type': 'comment',
                'body': comment.body,
                'permalink': f'https://reddit.com{comment.permalink}'
            })
    except Exception as e:
        print(f'Error fetching user content: {e}')
    return posts, comments

posts, comments = fetch_user_content(username)
all_content = posts + comments

print(f"Fetched {len(posts)} posts and {len(comments)} comments for user {username}.")

content_snippets = []
for idx, item in enumerate(all_content):
    if item['type'] == 'post':
        snippet = f"[POST {idx+1}] Title: {item['title']}\nBody: {item['body']}\nLink: {item['permalink']}"
    else:
        snippet = f"[COMMENT {idx+1}] {item['body']}\nLink: {item['permalink']}"
    content_snippets.append(snippet)

context = "\n\n".join(content_snippets)

persona_prompt = f"""
Given the following Reddit posts and comments, generate a detailed user persona for the user. For each characteristic (such as interests, personality, profession, etc.), cite the specific post or comment (by snippet or link) that supports it. Use the following format:

User Persona for u/{username}

- Characteristic: ...
  - Cited from: ... (include snippet or link)

Reddit Data:\n\n{context}
"""

persona_output = None
try:
    response = ollama.generate(model='llama3', prompt=persona_prompt)
    persona_output = response['response']
except Exception as e:
    print(f"Error generating persona with Ollama: {e}")

if persona_output:
    output_path = os.path.join('output', f'{username}_persona.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(persona_output)
    print(f"User persona saved to {output_path}")
else:
    print("Failed to generate user persona.") 