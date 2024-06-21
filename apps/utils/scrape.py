import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from newspaper import Article
import re
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime
import time
import requests
import random
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def format_date(month, day, year):
    return f"{month}/{day}/{year}" if month and day and year else ""

def clean_text(text):
    cleaned_text = re.sub(r'\[\\→\n\"/\]', '', text)
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

def fetch_article_content(url, snippet, retries=3):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    for attempt in range(retries):
        try:
            article = Article(url)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            article.download(input_html=response.text)
            article.parse()            
            article_html = article.html
            article_html = remove_unwanted_sentences_from_html(article_html)
            article.set_html(article_html)
            article.parse()

            authors = ', '.join(article.authors) 
            publish_date = article.publish_date
            top_image = article.top_image if re.search(IMAGE_EXTENSIONS_REGEX, article.top_image, re.IGNORECASE) else None

            full_content = article.text
            
            if not full_content.startswith(snippet):
                full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
            full_content = snippet + " " + full_content.strip()
            full_content = clean_text(full_content)
            
            article_word_count = len(full_content.split())
            logging.info(f"Article Length: {article_word_count} words")
            
            if article_word_count < 100:
                logging.info(f"Skipping article: '{url}' - Content too short.")
                return None, None, None, None

            return full_content, authors, publish_date, top_image
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for '{url}': {str(e)}")
            time.sleep(2 ** attempt) 
        except Exception as e:
            logging.error(f"Error fetching article content from '{url}': {str(e)}")
    logging.error(f"Failed to fetch article content from '{url}' after {retries} attempts.")
    return None, None, None, None

def convert_relative_date(date_str):
    if date_str:
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            return parsed_date.strftime("%Y-%m-%d")
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

        start_from = 9 
        
        params = {
            "q": keyword,
            "tbm": "nws",
            "engine": "google",
            "start":start_from,
            "num": "10",
            "tbs": tbs_param,
            "api_key": os.getenv('SERPAPI_KEY')
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]
        logging.info("news_results: %s", news_results)

        for news_item in news_results:
            if "date" in news_item:
                news_item["date"] = convert_relative_date(news_item["date"])

        response_data = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results}
            for future in as_completed(future_to_news_item):
                news_item = future_to_news_item[future]
                try:
                    full_content, authors, publish_date, top_image = future.result()
                    if full_content is not None and full_content != "":
                        article_word_count = len(full_content.split())
                        logging.info(f"Processing article: '{news_item['title']}' with {article_word_count} words")

                        news_item["full_content"] = full_content
                        news_item["authors"] = authors
                        news_item["publish_date"] = publish_date
                        news_item["top_image"] = top_image
                        response_data.append(news_item)
                    else:
                        logging.warning(f"Failed to fetch full content for '{news_item['title']}': No content available.")
                except Exception as e:
                    logging.error(f"Error processing article '{news_item['title']}': {str(e)}")

        return response_data
    except Exception as e:
        logging.error(f"Error in scrape_news: {str(e)}")
        raise e



