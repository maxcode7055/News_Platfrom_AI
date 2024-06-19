from flask import Flask, jsonify, request
from serpapi import GoogleSearch
from datetime import date
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)



# Funtion to take date as input from user
def format_date(month, day, year):
    return f"{month}/{day}/{year}" if month and day and year else ""

# Funtion to remove unnecessary symbols from textof full_content
def clean_text(text):
    cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
    return cleaned_text.strip()

# Search News API
@app.route('/search_news', methods=['POST'])
def search_news():
    try:
        data = request.json
        keyword = data.get('q')
        month = data.get('month')
        from_day = data.get('from_day')
        to_day = data.get('to_day')
        year = data.get('year')

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
            "q": keyword,     # News keyword to search
            "tbm": "nws",     # nws means news
            "num": "5",       # number of links we want to get scraped 
            "tbs": tbs_param, # To take date as input to scrape news accordingly
            "api_key": "93eed08042f625c377626ad343660e93aececc16f411a0aa2667840d201ea910"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]

        response_data = []
        for result in news_results:
            news_item = {
                "position": result["position"],
                "title": result["title"],
                "link": result["link"],
                "date": result["date"],
                "source": result["source"],
                "snippet": "",
                "thumbnail": result.get("thumbnail"),
                "full_content": ""
            }

            try:
                response = requests.get(result["link"])
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    # Remove unwanted tags and elements
                    for unwanted in soup(['header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']):
                        unwanted.decompose()
                    
                    # Extract snippet content
                    snippet = result.get("snippet") or ""
                    news_item["snippet"] = clean_text(snippet)

                    paragraphs = soup.find_all("p")
                    
                    # Concatenate paragraph texts
                    full_content = ""
                    for para in paragraphs:
                        para_text = para.get_text().strip()
                        if para_text:
                            full_content += para_text + " "  # Add paragraph
                    
                    # Clean up content
                    full_content = clean_text(full_content)
                    
                    # Ensure full_content starts with snippet text
                    if not full_content.startswith(news_item["snippet"]):
                        # Remove leading words until snippet text is at the start
                        full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(news_item["snippet"]), '', full_content, flags=re.IGNORECASE)
                        full_content = news_item["snippet"] + " " + full_content.strip()

                    news_item["full_content"] = full_content.strip()  # Remove leading/trailing whitespace

                else:
                    news_item["full_content"] = f"Failed to fetch article content: {response.status_code}"
            except Exception as e:
                news_item["full_content"] = f"Error fetching article content: {str(e)}"

            response_data.append(news_item)

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


