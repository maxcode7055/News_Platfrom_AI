# from serpapi import GoogleSearch
# from bs4 import BeautifulSoup
# import requests
# import re
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed

# load_dotenv()

# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()


# def fetch_article_content(url, snippet):
#     try:
#         headers = {
#             'User-Agent': 'Your User Agent String'  # Provide a valid User-Agent header
#         }
#         response = requests.get(url, headers=headers)

#         # Handle HTTP 403 explicitly
#         if response.status_code == 403:
#             return None, f"Failed to fetch article content: Access forbidden (403)"

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, "html.parser")

#             for unwanted in soup(['header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']):
#                 unwanted.decompose()

#             paragraphs = soup.find_all("p")
#             full_content = ""
#             for para in paragraphs:
#                 para_text = para.get_text().strip()
#                 if para_text:
#                     full_content += para_text + " "

#             full_content = clean_text(full_content)

#             # Ensure full_content starts with snippet text
#             if not full_content.startswith(snippet):
#                 # Remove leading words until snippet text is at the start
#                 full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#                 full_content = snippet + " " + full_content.strip()

#             return full_content, None

#         else:
#             return None, f"Failed to fetch article content: {response.status_code}"

#     except Exception as e:
#         return None, f"Error fetching article content: {str(e)}"


# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google", 
#             "num": "10",  # Fetching 10 results for faster processing
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 full_content, error_message = future.result()

#                 if full_content is not None and full_content != "":
#                     # Check if full_content has less than 30 words
#                     if len(full_content.split()) >= 30:
#                         news_item["full_content"] = full_content
#                         response_data.append(news_item)
#                     else:
#                         print(f"Skipping '{news_item['title']}': Full content has less than 30 words.")
#                 else:
#                     # Optionally, you can include error handling or logging here
#                     print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

#         return response_data

#     except Exception as e:
#         raise e



# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup

# load_dotenv()

# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()

# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     for p in soup.find_all('p'):
#         if '©' in p.get_text() or 'Read' in p.get_text():
#             p.decompose()
#     return str(soup)

# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()
#         full_content = article.text

#         # Ensure full_content starts with snippet text
#         if not full_content.startswith(snippet):
#             # Remove leading words until snippet text is at the start
#             full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#             full_content = snippet + " " + full_content.strip()

#         full_content = clean_text(full_content)
        
#         print(f"Article Length: {len(full_content.split())} words")  # Debugging print statement

#         return full_content, None
#     except Exception as e:
#         return None, f"Error fetching article content: {str(e)}"

# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "10",  # Fetching 10 results for faster processing
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 full_content, error_message = future.result()

#                 if full_content is not None and full_content != "":
#                     article_word_count = len(full_content.split())
#                     print(f"Processing article: '{news_item['title']}' with {article_word_count} words")  # Debugging print statement
#                     # Check if full_content has less than 100 words
#                     if article_word_count >= 100:
#                         news_item["full_content"] = full_content
#                         response_data.append(news_item)
#                     else:
#                         print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
#                 else:
#                     # Optionally, you can include error handling or logging here
#                     print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

#         return response_data

#     except Exception as e:
#         raise e



# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup

# load_dotenv()

# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()

# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     for p in soup.find_all('p'):
#         if '©' in p.get_text() or 'Read' in p.get_text() or '@' in p.get_text():
#             p.decompose()
#     return str(soup)

# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()

#         # Extract additional data
#         authors = article.authors
#         publish_date = article.publish_date
#         top_image = article.top_image

#         full_content = article.text

#         # Ensure full_content starts with snippet text
#         if not full_content.startswith(snippet):
#             # Remove leading words until snippet text is at the start
#             full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#             full_content = snippet + " " + full_content.strip()

#         full_content = clean_text(full_content)
        
#         print(f"Article Length: {len(full_content.split())} words")  # Debugging print statement

#         return full_content, authors, publish_date, top_image, None
#     except Exception as e:
#         return None, None, None, None, f"Error fetching article content: {str(e)}"

# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "10",  # Fetching 10 results for faster processing
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 full_content, authors, publish_date, top_image, error_message = future.result()

#                 if full_content is not None and full_content != "":
#                     article_word_count = len(full_content.split())
#                     print(f"Processing article: '{news_item['title']}' with {article_word_count} words")  # Debugging print statement
#                     # Check if full_content has less than 100 words
#                     if article_word_count >= 100:
#                         news_item["full_content"] = full_content
#                         news_item["authors"] = authors
#                         news_item["publish_date"] = publish_date
#                         news_item["top_image"] = top_image
#                         response_data.append(news_item)
#                     else:
#                         print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
#                 else:
#                     # Optionally, you can include error handling or logging here
#                     print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

#         return response_data

#     except Exception as e:
#         raise e


# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup
# import re

# IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

# load_dotenv()

# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()

# def remove_unwanted_tags(soup):
#     # Define list of tags to remove
#     unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']

#     for tag in unwanted_tags:
#         for el in soup.find_all(tag):
#             el.decompose()

#     return soup

# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     # Remove unwanted tags
#     soup = remove_unwanted_tags(soup)
    
#     return str(soup)

# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()

#         # Extract additional data
#         authors = article.authors
#         publish_date = article.publish_date
#         top_image = article.top_image

#         # Validate top_image format
#         if top_image and re.search(IMAGE_EXTENSIONS_REGEX, top_image, re.IGNORECASE):
#             full_content = article.text

#             # Ensure full_content starts with snippet text
#             if not full_content.startswith(snippet):
#                 # Remove leading words until snippet text is at the start
#                 full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#                 full_content = snippet + " " + full_content.strip()

#             full_content = clean_text(full_content)
            
#             print(f"Article Length: {len(full_content.split())} words")  # Debugging print statement

#             return full_content, authors, publish_date, top_image, None
#         else:
#             return None, None, None, None, "Invalid or missing top_image URL"

#     except Exception as e:
#         return None, None, None, None, f"Error fetching article content: {str(e)}"

# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "10",  # Fetching 10 results for faster processing
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 full_content, authors, publish_date, top_image, error_message = future.result()

#                 if full_content is not None and full_content != "":
#                     article_word_count = len(full_content.split())
#                     print(f"Processing article: '{news_item['title']}' with {article_word_count} words")  # Debugging print statement
#                     # Check if full_content has less than 100 words
#                     if article_word_count >= 100:
#                         news_item["full_content"] = full_content
#                         news_item["authors"] = authors
#                         news_item["publish_date"] = publish_date
#                         news_item["top_image"] = top_image
#                         response_data.append(news_item)
#                     else:
#                         print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
#                 else:
#                     # Optionally, you can include error handling or logging here
#                     print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

#         return response_data

#     except Exception as e:
#         raise e


# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup
# import dateparser
# from datetime import datetime

# IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

# load_dotenv()

# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()

# def remove_unwanted_tags(soup):
#     unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']

#     for tag in unwanted_tags:
#         for el in soup.find_all(tag):
#             el.decompose()

#     return soup

# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     soup = remove_unwanted_tags(soup)
    
#     return str(soup)

# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()

#         authors = article.authors
#         publish_date = article.publish_date
#         top_image = article.top_image

#         if top_image and re.search(IMAGE_EXTENSIONS_REGEX, top_image, re.IGNORECASE):
#             full_content = article.text

#             if not full_content.startswith(snippet):
#                 full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#                 full_content = snippet + " " + full_content.strip()

#             full_content = clean_text(full_content)
            
#             print(f"Article Length: {len(full_content.split())} words")  

#             return full_content, authors, publish_date, top_image, None
#         else:
#             return None, None, None, None, "Invalid or missing top_image URL"

#     except Exception as e:
#         return None, None, None, None, f"Error fetching article content: {str(e)}"

# def convert_relative_date(date_str):
#     if date_str:
#         parsed_date = dateparser.parse(date_str)
#         if parsed_date:
#             return parsed_date.strftime("%Y-%m-%d")
#     return date_str

# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "20",  
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]
#         print("news_results----------------------------------------->",news_results)

#         # Convert relative dates to absolute dates
#         for news_item in news_results:
#             if "date" in news_item:
#                 news_item["date"] = convert_relative_date(news_item["date"])

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results[:10]}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 full_content, authors, publish_date, top_image, error_message = future.result()

#                 if full_content is not None and full_content != "":
#                     article_word_count = len(full_content.split())
#                     print(f"Processing article: '{news_item['title']}' with {article_word_count} words")  # Debugging print statement
#                     # Check if full_content has less than 100 words
#                     if article_word_count >= 10:
#                         news_item["full_content"] = full_content
#                         news_item["authors"] = authors
#                         news_item["publish_date"] = publish_date
#                         news_item["top_image"] = top_image
#                         response_data.append(news_item)
#                     else:
#                         print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
#                 else:
#                     # Optionally, you can include error handling or logging here
#                     print(f"Failed to fetch full content for '{news_item['title']}': {error_message}")

#         return response_data

#     except Exception as e:
#         raise e



# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup
# import dateparser
# from datetime import datetime

# # Load environment variables
# load_dotenv()

# # Define a regex for valid image extensions
# IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

# # Function to format the date into a specific string format
# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# # Function to clean text by removing unwanted characters
# def clean_text(text):
#     cleaned_text = re.sub(r'\[\\→\n\"/\]', '', text)
#     return cleaned_text.strip()

# # Function to remove unwanted HTML tags
# def remove_unwanted_tags(soup):
#     unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']
#     for tag in unwanted_tags:
#         for el in soup.find_all(tag):
#             el.decompose()
#     return soup

# # Function to remove unwanted sentences from HTML content
# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     soup = remove_unwanted_tags(soup)
#     return str(soup)

# # Function to fetch article content from a given URL
# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
        
#         # Remove unwanted HTML tags before parsing again
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()

#         # Extracting article metadata
#         authors = article.authors
#         publish_date = article.publish_date
#         top_image = article.top_image if re.search(IMAGE_EXTENSIONS_REGEX, article.top_image, re.IGNORECASE) else None

#         # Fetch full content
#         full_content = article.text
        
#         # Ensure snippet is included in full content
#         if not full_content.startswith(snippet):
#             full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#         full_content = snippet + " " + full_content.strip()
#         full_content = clean_text(full_content)
        
#         # Print the length of the article for debugging
#         print(f"Article Length: {len(full_content.split())} words")
        
#         return full_content, authors, publish_date, top_image
#     except Exception as e:
#         print(f"Error fetching article content: {str(e)}")
#         return None, None, None, None

# # Function to convert relative date to an absolute date
# def convert_relative_date(date_str):
#     if date_str:
#         parsed_date = dateparser.parse(date_str)
#         if parsed_date:
#             return parsed_date.strftime("%Y-%m-%d")
#     return date_str

# # Function to scrape news articles based on a keyword and date range
# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         # Construct the Google Search parameter for date filtering
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         # Setup parameters for the Google Search API
#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "20",
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         # Perform the search using SerpAPI
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]
#         print("news_results----------------------------------------->", news_results)

#         # Convert relative dates to absolute dates
#         for news_item in news_results:
#             if "date" in news_item:
#                 news_item["date"] = convert_relative_date(news_item["date"])

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching of article content
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 try:
#                     full_content, authors, publish_date, top_image = future.result()
#                     if full_content is not None and full_content != "":
#                         article_word_count = len(full_content.split())
#                         print(f"Processing article: '{news_item['title']}' with {article_word_count} words")

#                         # Skip articles with less than 100 words
#                         if article_word_count >= 100:
#                             news_item["full_content"] = full_content
#                             news_item["authors"] = authors
#                             news_item["publish_date"] = publish_date
#                             news_item["top_image"] = top_image
#                             response_data.append(news_item)
#                         else:
#                             print(f"Skipping '{news_item['title']}': Full content has less than 100 words.")
#                     else:
#                         print(f"Failed to fetch full content for '{news_item['title']}': No content available.")
#                 except Exception as e:
#                     print(f"Error processing article '{news_item['title']}': {str(e)}")

#         return response_data
#     except Exception as e:
#         print(f"Error in scrape_news: {str(e)}")
#         raise e


# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup
# import dateparser
# from datetime import datetime

# # Load environment variables
# load_dotenv()

# # Define a regex for valid image extensions
# IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

# # Function to format the date into a specific string format
# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# # Function to clean text by removing unwanted characters
# def clean_text(text):
#     cleaned_text = re.sub(r'\[\\→\n\"/\]', '', text)
#     return cleaned_text.strip()

# # Function to remove unwanted HTML tags
# def remove_unwanted_tags(soup):
#     unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']
#     for tag in unwanted_tags:
#         for el in soup.find_all(tag):
#             el.decompose()
#     return soup

# # Function to remove unwanted sentences from HTML content
# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     soup = remove_unwanted_tags(soup)
#     return str(soup)

# # Function to fetch article content from a given URL
# def fetch_article_content(url, snippet):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
        
#         # Remove unwanted HTML tags before parsing again
#         article_html = article.html
#         article_html = remove_unwanted_sentences_from_html(article_html)
#         article.set_html(article_html)
#         article.parse()

#         # Extracting article metadata
#         authors = article.authors
#         publish_date = article.publish_date
#         top_image = article.top_image if re.search(IMAGE_EXTENSIONS_REGEX, article.top_image, re.IGNORECASE) else None

#         # Fetch full content
#         full_content = article.text
        
#         # Ensure snippet is included in full content
#         if not full_content.startswith(snippet):
#             full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#         full_content = snippet + " " + full_content.strip()
#         full_content = clean_text(full_content)
        
#         # Print the length of the article for debugging
#         article_word_count = len(full_content.split())
#         print(f"Article Length: {article_word_count} words")
        
#         # Skip articles with less than 100 words
#         if article_word_count < 100:
#             print(f"Skipping article: '{url}' - Content too short.")
#             return None, None, None, None

#         return full_content, authors, publish_date, top_image
#     except Exception as e:
#         print(f"Error fetching article content from '{url}': {str(e)}")
#         return None, None, None, None

# # Function to convert relative date to an absolute date
# def convert_relative_date(date_str):
#     if date_str:
#         parsed_date = dateparser.parse(date_str)
#         if parsed_date:
#             return parsed_date.strftime("%Y-%m-%d")
#     return date_str

# # Function to scrape news articles based on a keyword and date range
# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         # Construct the Google Search parameter for date filtering
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         # Setup parameters for the Google Search API
#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "20",
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         # Perform the search using SerpAPI
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]
#         print("news_results----------------------------------------->", news_results)

#         # Convert relative dates to absolute dates
#         for news_item in news_results:
#             if "date" in news_item:
#                 news_item["date"] = convert_relative_date(news_item["date"])

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching of article content
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 try:
#                     full_content, authors, publish_date, top_image = future.result()
#                     if full_content is not None and full_content != "":
#                         article_word_count = len(full_content.split())
#                         print(f"Processing article: '{news_item['title']}' with {article_word_count} words")

#                         news_item["full_content"] = full_content
#                         news_item["authors"] = authors
#                         news_item["publish_date"] = publish_date
#                         news_item["top_image"] = top_image
#                         response_data.append(news_item)
#                     else:
#                         print(f"Failed to fetch full content for '{news_item['title']}': No content available.")
#                 except Exception as e:
#                     print(f"Error processing article '{news_item['title']}': {str(e)}")

#         return response_data
#     except Exception as e:
#         print(f"Error in scrape_news: {str(e)}")
#         raise e



# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from newspaper import Article
# import re
# from bs4 import BeautifulSoup
# import dateparser
# from datetime import datetime
# import time
# import requests
# import random

# # Load environment variables
# load_dotenv()

# # Define a regex for valid image extensions
# IMAGE_EXTENSIONS_REGEX = r'\.(jpg|jpeg|png|webp|avif)$'

# # List of user agents to rotate
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
# ]

# # Function to format the date into a specific string format
# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# # Function to clean text by removing unwanted characters
# def clean_text(text):
#     cleaned_text = re.sub(r'\[\\→\n\"/\]', '', text)
#     return cleaned_text.strip()

# # Function to remove unwanted HTML tags
# def remove_unwanted_tags(soup):
#     unwanted_tags = ['ul', 'header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']
#     for tag in unwanted_tags:
#         for el in soup.find_all(tag):
#             el.decompose()
#     return soup

# # Function to remove unwanted sentences from HTML content
# def remove_unwanted_sentences_from_html(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     soup = remove_unwanted_tags(soup)
#     return str(soup)

# # Function to fetch article content from a given URL with retry mechanism
# def fetch_article_content(url, snippet, retries=3):
#     headers = {'User-Agent': random.choice(USER_AGENTS)}
#     try:
#         for attempt in range(retries):
#             try:
#                 article = Article(url)
#                 article.download(input_html=requests.get(url, headers=headers).text)
#                 article.parse()
                
#                 # Remove unwanted HTML tags before parsing again
#                 article_html = article.html
#                 article_html = remove_unwanted_sentences_from_html(article_html)
#                 article.set_html(article_html)
#                 article.parse()

#                 # Extracting article metadata
#                 authors = article.authors
#                 publish_date = article.publish_date
#                 top_image = article.top_image if re.search(IMAGE_EXTENSIONS_REGEX, article.top_image, re.IGNORECASE) else None

#                 # Fetch full content
#                 full_content = article.text
                
#                 # Ensure snippet is included in full content
#                 if not full_content.startswith(snippet):
#                     full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(snippet), '', full_content, flags=re.IGNORECASE)
#                 full_content = snippet + " " + full_content.strip()
#                 full_content = clean_text(full_content)
                
#                 # Print the length of the article for debugging
#                 article_word_count = len(full_content.split())
#                 print(f"Article Length: {article_word_count} words")
                
#                 # Skip articles with less than 100 words
#                 if article_word_count < 100:
#                     print(f"Skipping article: '{url}' - Content too short.")
#                     return None, None, None, None

#                 return full_content, authors, publish_date, top_image
#             except requests.exceptions.RequestException as e:
#                 print(f"Attempt {attempt + 1} failed for '{url}': {str(e)}")
#                 time.sleep(2 ** attempt)  # Exponential backoff
#                 continue  # Retry the request
#         print(f"Failed to fetch article content from '{url}' after {retries} attempts.")
#         return None, None, None, None
#     except Exception as e:
#         print(f"Error fetching article content from '{url}': {str(e)}")
#         return None, None, None, None

# # Function to convert relative date to an absolute date
# def convert_relative_date(date_str):
#     if date_str:
#         parsed_date = dateparser.parse(date_str)
#         if parsed_date:
#             return parsed_date.strftime("%Y-%m-%d")
#     return date_str

# # Function to scrape news articles based on a keyword and date range
# def scrape_news(keyword, month, from_day, to_day, year):
#     try:
#         # Construct the Google Search parameter for date filtering
#         tbs_param = ""
#         if month or from_day or to_day or year:
#             if month and from_day and to_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)},cd_max:{format_date(month, to_day, year)}"
#             elif month and from_day and year:
#                 tbs_param = f"cdr:1,cd_min:{format_date(month, from_day, year)}"
#             elif month and to_day and year:
#                 tbs_param = f"cdr:1,cd_max:{format_date(month, to_day, year)}"
#             elif year:
#                 tbs_param = f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"

#         # Setup parameters for the Google Search API
#         params = {
#             "q": keyword,
#             "tbm": "nws",
#             "engine": "google",
#             "num": "20",
#             "tbs": tbs_param,
#             "api_key": os.getenv('SERPAPI_KEY')
#         }

#         # Perform the search using SerpAPI
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]
#         print("news_results----------------------------------------->", news_results)

#         # Convert relative dates to absolute dates
#         for news_item in news_results:
#             if "date" in news_item:
#                 news_item["date"] = convert_relative_date(news_item["date"])

#         response_data = []

#         # Using ThreadPoolExecutor for parallel fetching of article content
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future_to_news_item = {executor.submit(fetch_article_content, result["link"], result.get("snippet", "")): result for result in news_results}
#             for future in as_completed(future_to_news_item):
#                 news_item = future_to_news_item[future]
#                 try:
#                     full_content, authors, publish_date, top_image = future.result()
#                     if full_content is not None and full_content != "":
#                         article_word_count = len(full_content.split())
#                         print(f"Processing article: '{news_item['title']}' with {article_word_count} words")

#                         news_item["full_content"] = full_content
#                         news_item["authors"] = authors
#                         news_item["publish_date"] = publish_date
#                         news_item["top_image"] = top_image
#                         response_data.append(news_item)
#                     else:
#                         print(f"Failed to fetch full content for '{news_item['title']}': No content available.")
#                 except Exception as e:
#                     print(f"Error processing article '{news_item['title']}': {str(e)}")

#         return response_data
#     except Exception as e:
#         print(f"Error in scrape_news: {str(e)}")
#         raise e

