from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from newspaper import Article
import re
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime

IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

load_dotenv()

def format_date(month, day, year):
    return f"{month}/{day}/{year}" if month and day and year else ""

def clean_text(text):
    cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
    return cleaned_text.strip()

def remove_unwanted_tags(soup):
    unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']

    for tag in unwanted_tags:
        for el in soup.find_all(tag):
            el.decompose()

    return soup

def remove_unwanted_sentences_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    soup = remove_unwanted_tags(soup)
    
    return str(soup)

def fetch_article_content(url, snippet):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article_html = article.html
        article_html = remove_unwanted_sentences_from_html(article_html)
        article.set_html(article_html)
        article.parse()

        authors = article.authors
        publish_date = article.publish_date
        top_image = article.top_image

        if top_image and re.search(IMAGE_EXTENSIONS_REGEX, top_image, re.IGNORECASE):
            full_content = article.text

            if not full_content.startswith(snippet):
                full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
                full_content = snippet + " " + full_content.strip()

            full_content = clean_text(full_content)
            
            print(f"Article Length: {len(full_content.split())} words")  

            return full_content, authors, publish_date, top_image, None
        else:
            return None, None, None, None, "Invalid or missing top_image URL"

    except Exception as e:
        return None, None, None, None, f"Error fetching article content: {str(e)}"

def convert_relative_date(date_str):
    if date_str:
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    return date_str

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
            "engine": "google",
            "num": "10",  
            "tbs": tbs_param,
            "api_key": os.getenv('SERPAPI_KEY')
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]

        # Convert relative dates to absolute dates
        for news_item in news_results:
            if "date" in news_item:
                news_item["date"] = convert_relative_date(news_item["date"])

        response_data = []

        # Using ThreadPoolExecutor for parallel fetching
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
            for future in as_completed(future_to_news_item):
                news_item = future_to_news_item[future]
                full_content, authors, publish_date, top_image, error_message = future.result()

                if full_content is not None and full_content != "":
                    article_word_count = len(full_content.split())
                    print(f"Processing article: '{news_item['title']}' with {article_word_count} words")  # Debugging print statement
                    # Check if full_content has less than 100 words
                    if article_word_count >= 100:
                        news_item["full_content"] = full_content
                        news_item["authors"] = authors
                        news_item["publish_date"] = publish_date
                        news_item["top_image"] = top_image
                        response_data.append(news_item)
                    else:
                        print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
                else:
                    # Optionally, you can include error handling or logging here
                    print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

        return response_data

    except Exception as e:
        raise e

