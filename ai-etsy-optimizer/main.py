import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# Load environment variables from .env if present
load_dotenv()

# Set OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

system_prompt = """You are an Etsy Listing Optimizer.
When given a raw product title, description and tags, output a complete, optimized listing in this exact format:

TITLE:
<optimized title, 120–140 chars, front-loaded with keywords>

DESCRIPTION:
<optimized description with recommended headers and bullet points>

TAGS:
<13 unique, lowercase, comma-separated tags, each under 20 characters>

Rules:
• Do not invent any details not supplied.
• Do not include prohibited items.
• Follow the character and formatting requirements strictly.
"""

def optimize_listing(title, description, tags):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": 
            f"Raw title: {title}\n"
            f"Description: {description}\n"
            f"Tags: {tags}"
        }
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=800,
        temperature=0.7
    )
    return resp.choices[0].message.content

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json(force=True)
    result = optimize_listing(
        data.get("title", ""),
        data.get("description", ""),
        data.get("tags", "")
    )
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
