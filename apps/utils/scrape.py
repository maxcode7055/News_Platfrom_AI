import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()
serpapi_key = os.getenv('SERPAPI_KEY')

def search_all_links(base_url, keyword, num_results=5):
    api_key = serpapi_key
    search_engine = "google"
    serpapi_url = "https://serpapi.com/search"

    query = f"{keyword} site:{base_url}"

    params = {
        "q": query,
        "num": num_results,
        "api_key": api_key,
        "engine": search_engine,
    }

    response = requests.get(serpapi_url, params=params)

    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        links = [result['link'] for result in results]
        print(links, "/" * 80)
        return links
    else:
        print("Error occurred while fetching search results.")
        return None

def scrape_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page content: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        elements = soup.find_all(["div"])

        text = '\n'.join([element.get_text(separator=" ", strip=True) for element in elements])

        return text.strip()
    except Exception as e:
        print(f"Error occurred while scraping the article: {e}")
        return None

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved article to {filename}")

def scrape_data(keyword):
    base_url = "timesofindia.indiatimes.com"
    all_links = search_all_links(base_url, keyword, num_results=10)

    scraped_data = []
    if all_links:
        print(f"All links related to '{keyword}':")
        for link in all_links:
            print(link)

        print("\nScraping articles...\n")

        for i, url in enumerate(all_links):
            print(f"Scraping URL {i + 1}: {url}")
            text = scrape_text_from_url(url)
            if text:
                filename = f"article_{i+1}.txt"  
                save_text_to_file(text, filename)
                
                scraped_data.append({
                    'url': url,
                    'text': text
                })

    return scraped_data
