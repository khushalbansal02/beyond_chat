# Reddit User Persona Generator

This project generates a detailed user persona for any Reddit user by analyzing their posts and comments using a local LLM (Llama 3 via Ollama). Each persona trait is cited with the specific post or comment it was derived from.

## Features
- Scrapes posts and comments from any Reddit user profile
- Uses a local LLM (Llama 3 via Ollama) to generate a persona with citations
- Outputs the persona to a text file in the `output/` directory

## Setup

### 1. Clone the repository
```
git clone <your-repo-url>
cd beyondchat
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Get Reddit API Credentials
- **Reddit API:**
  1. Go to https://www.reddit.com/prefs/apps
  2. Click "create another app"
  3. Set type to "script"
  4. Note your `client_id`, `client_secret`, and set a `user_agent` (any string)

### 4. Set Reddit API Credentials
Create a `.env` file in the project root with:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### 5. Install and Run Ollama (for Local LLM)
- Download and install Ollama from [https://ollama.com/](https://ollama.com/)
- Add Ollama to your system PATH if needed (see their docs)
- Pull the Llama 3 model:
  ```
  ollama pull llama3
  ```
- Make sure the Ollama server is running (usually starts automatically)

## Usage
```
python reddit_persona.py
```
- Enter the Reddit user profile URL when prompted (e.g., `https://www.reddit.com/user/kojied/`)
- The script will fetch posts/comments, generate a persona, and save it to `output/<username>_persona.txt`

## Notes
- You can adjust the number of posts/comments fetched by editing the `limit` parameter in the script.
- The script uses the local Llama 3 model via Ollama by default.

## Example Output
```
User Persona for u/exampleuser
- Characteristic: Interest in technology
  - Cited from: "I love building PCs..." (https://reddit.com/r/buildapc/comments/xyz/abc)
...
```

---
Feel free to modify or extend the script for your needs! 