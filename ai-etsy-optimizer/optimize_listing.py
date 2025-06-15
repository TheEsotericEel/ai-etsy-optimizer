import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Quick local test—set your key here (remove before production)
os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.getenv('OPENAI_API_KEY')


system_prompt = """You are an Etsy Listing Optimizer.
When given a raw product title, description and tags, output a complete, optimized listing in this exact format:

TITLE:
<optimized title, 120-140 chars, front-loaded with keywords>

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
        {"role": "system",  "content": system_prompt},
        {"role": "user",    "content":
           f"Raw title: {title}\n"
           f"Description: {description}\n"
           f"Tags: {tags}"
        }
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(optimize_listing(
        "Handcrafted Leather Wallet",
        "A slim, full-grain leather wallet with 6 card slots and a cash pocket.",
        "leather, wallet, slim, handmade"
    ))
