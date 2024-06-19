from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import requests
import re
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

def format_date(month, day, year):
    return f"{month}/{day}/{year}" if month and day and year else ""

def clean_text(text):
    cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
    return cleaned_text.strip()


def fetch_article_content(url, snippet):
    try:
        headers = {
            'User-Agent': 'Your User Agent String'  # Provide a valid User-Agent header
        }
        response = requests.get(url, headers=headers)

        # Handle HTTP 403 explicitly
        if response.status_code == 403:
            return None, f"Failed to fetch article content: Access forbidden (403)"

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for unwanted in soup(['header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']):
                unwanted.decompose()

            paragraphs = soup.find_all("p")
            full_content = ""
            for para in paragraphs:
                para_text = para.get_text().strip()
                if para_text:
                    full_content += para_text + " "

            full_content = clean_text(full_content)

            # Ensure full_content starts with snippet text
            if not full_content.startswith(snippet):
                # Remove leading words until snippet text is at the start
                full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
                full_content = snippet + " " + full_content.strip()

            return full_content, None

        else:
            return None, f"Failed to fetch article content: {response.status_code}"

    except Exception as e:
        return None, f"Error fetching article content: {str(e)}"


def scrape_news(keyword, month, from_day, to_day, year):
    try:
        tbs_param = ""
        if month or from_day or to_day or year:
            if month and from_day and to_day and year:
                tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
            elif month and from_day and year:
                tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
            elif month and to_day and year:
                tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
            elif year:
                tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

        params = {
            "q": keyword,
            "tbm": "nws",
            "num": "10",  # Fetching 10 results for faster processing
            "tbs": tbs_param,
            "api_key": os.getenv('SERPAPI_KEY')
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]

        response_data = []

        # Using ThreadPoolExecutor for parallel fetching
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
            for future in as_completed(future_to_news_item):
                news_item = future_to_news_item[future]
                full_content, error_message = future.result()

                if full_content is not None and full_content != "":
                    # Check if full_content has less than 30 words
                    if len(full_content.split()) >= 30:
                        news_item["full_content"] = full_content
                        response_data.append(news_item)
                    else:
                        print(f"Skipping '{news_item['title']}': Full content has less than 30 words.")
                else:
                    # Optionally, you can include error handling or logging here
                    print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

        return response_data

    except Exception as e:
        raise e
