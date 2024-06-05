import requests
from bs4 import BeautifulSoup
import os

def search_all_links(base_url, keyword, num_results=5):
    api_key = "31b31eafbec0aedaaf48e8ebf8d2baa55faff180c67ae66e95007895ddc560c1"
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
        print(links,"/"*80)
        return links
    else:
        print("Error occurred while fetching search results.")
        return None


def scrape_text_from_url(url):
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page content: {response.status_code}")

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Define a function to remove unwanted elements like scripts and styles
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', '[document]', 'noscript']):
            script_or_style.extract()

        # Extract text from all elements that may contain content
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', "div"])

        # Combine text from all selected elements
        text = '\n'.join([element.get_text(separator=" ", strip=True) for element in elements])

        return text.strip()
    except Exception as e:
        print(f"Error occurred while scraping the article: {e}")
        return None


def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def main():
    base_url = "timesofindia.indiatimes.com"
    keyword = "cricket"
    all_links = search_all_links(base_url, keyword, num_results=10)

    if all_links:
        print("All links related to 'cricket':")
        for link in all_links:
            print(link)

        print("\nScraping articles...\n")
        
        for i, url in enumerate(all_links):
            print(f"Scraping URL {i + 1}: {url}")
            text = scrape_text_from_url(url)
            if text:
                filename = f"article_{i + 1}.txt"
                save_text_to_file(text, filename)
                print(f"Saved scraped text to {filename}\n")


if __name__ == "__main__":
    main()
