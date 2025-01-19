import re
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def identify_css_selectors_from_html(html_content: str):
    """
    Uses OpenAI to analyze the HTML content and identify CSS selectors for reviews and pagination.

    Returns a dictionary with the following keys:
      - "review_container": The outer container for one review.
      - "title": The review title (if available).
      - "body": The main text of the review.
      - "rating": The star or numeric rating element.
      - "reviewer_name": The name/username of the reviewer.
      - "next_button": The clickable element that leads to the next page of reviews.

    Notes:
      - If the same class/ID is used for both "previous" and "next" buttons, 
        the model should only return the 'next_button' or set it to null if it cannot differentiate.
    """
    try:
        # Define the prompt for OpenAI
        prompt = f"""
You are a web-scraping assistant analyzing a product reviews page's HTML.

**Task:**
1. Identify the CSS selectors (class, id, or tag) for:
   - "review_container": The outer container for one review.
   - "title": The review title (if available).
   - "body": The main text of the review.
   - "rating": The star or numeric rating element.
   - "reviewer_name": The name/username of the reviewer.
   - "next_button": The clickable element that leads to the next page of reviews.

2. **Important**:
   - The same class or ID may be used for both "previous" and "next" buttons.
   - You must **only return** the selector for the **next** button (ignore or set to null if unsure).
   - If you cannot tell next from previous, set "next_button" to null.

3. **Output Requirements**:
   - Return **only** valid JSON (no extra text or explanation).
   - The JSON must have exactly these keys:
       "review_container", "title", "body", "rating", "reviewer_name", "next_button".
   - If you cannot find a valid selector for any of these, set it to null.
   - Do NOT use the sibling combinator '+' or '++'.

**HTML Content**:
{html_content}
"""
        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model version available to you
            messages=[
                {"role": "system", "content": "You are a web scraping assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Find and extract the JSON portion from the response
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in OpenAI response.")

        # Parse the JSON into a Python dictionary
        selectors = json.loads(json_match.group(0))
        return selectors

    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        return None
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None
