from shortGPT.gpt import gpt_utils
import json

def generate_title_description_dict(content):
    title = f"Exploring: {content[:50]}..."  # Use the first 50 chars of content
    description = f"This video discusses {content[:100]}... Stay tuned!"
    return title, description
