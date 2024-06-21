# from flask import Flask, jsonify, request
# from serpapi import GoogleSearch
# from datetime import date
# from bs4 import BeautifulSoup
# import requests
# import re

# app = Flask(__name__)



# # Funtion to take date as input from user
# def format_date(month, day, year):
#     return f"{month}/{day}/{year}" if month and day and year else ""

# # Funtion to remove unnecessary symbols from textof full_content
# def clean_text(text):
#     cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
#     return cleaned_text.strip()

# # Search News API
# @app.route('/search_news', methods=['POST'])
# def search_news():
#     try:
#         data = request.json
#         keyword = data.get('q')
#         month = data.get('month')
#         from_day = data.get('from_day')
#         to_day = data.get('to_day')
#         year = data.get('year')

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
#             "q": keyword,     # News keyword to search
#             "tbm": "nws",     # nws means news
#             "num": "5",       # number of links we want to get scraped 
#             "tbs": tbs_param, # To take date as input to scrape news accordingly
#             "api_key": "93eed08042f625c377626ad343660e93aececc16f411a0aa2667840d201ea910"
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         news_results = results["news_results"]

#         response_data = []
#         for result in news_results:
#             news_item = {
#                 "position": result["position"],
#                 "title": result["title"],
#                 "link": result["link"],
#                 "date": result["date"],
#                 "source": result["source"],
#                 "snippet": "",
#                 "thumbnail": result.get("thumbnail"),
#                 "full_content": ""
#             }

#             try:
#                 response = requests.get(result["link"])
#                 if response.status_code == 200:
#                     soup = BeautifulSoup(response.content, "html.parser")
                    
#                     # Remove unwanted tags and elements
#                     for unwanted in soup(['header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']):
#                         unwanted.decompose()
                    
#                     # Extract snippet content
#                     snippet = result.get("snippet") or ""
#                     news_item["snippet"] = clean_text(snippet)

#                     paragraphs = soup.find_all("p")
                    
#                     # Concatenate paragraph texts
#                     full_content = ""
#                     for para in paragraphs:
#                         para_text = para.get_text().strip()
#                         if para_text:
#                             full_content += para_text + " "  # Add paragraph
                    
#                     # Clean up content
#                     full_content = clean_text(full_content)
                    
#                     # Ensure full_content starts with snippet text
#                     if not full_content.startswith(news_item["snippet"]):
#                         # Remove leading words until snippet text is at the start
#                         full_content = re.sub(r'^.*?(?:\b%s\b\s*)' % re.escape(news_item["snippet"]), '', full_content, flags=re.IGNORECASE)
#                         full_content = news_item["snippet"] + " " + full_content.strip()

#                     news_item["full_content"] = full_content.strip()  # Remove leading/trailing whitespace

#                 else:
#                     news_item["full_content"] = f"Failed to fetch article content: {response.status_code}"
#             except Exception as e:
#                 news_item["full_content"] = f"Error fetching article content: {str(e)}"

#             response_data.append(news_item)

#         return jsonify(response_data)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



# import newspaper
# from newspaper import Article

# # Create an Article object using the URL
# url = 'https://www.nytimes.com/2024/06/19/opinion/democracy-partisanship-political-hatred.html'
# article = newspaper.Article(url)

# # Download and parse the article
# article.download()
# article.parse()

# # Print various attributes of the article
# print("Authors:", article.authors)
# print("Publish Date:", article.publish_date)
# print("Text:", article.text)
# print("Top Image:", article.top_image)
# print("Movies:", article.movies)

# # Perform natural language processing (NLP) on the article
# article.nlp()
# print("Keywords:", article.keywords)
# print("Summary:", article.summary)



# from deep_translator import ChatGptTranslator

# text = """
# Yanna Krupnikov probes the motivations of Americans who avoid politics — but often vote. ezra kleinFrom New York Times Opinion, this is “The Ezra Klein Show.” If you are listening to this show, you’re an odd duck. I mean, I’m an odd duck, too. But if you’re here, you can probably, say, list the Trump trials off the top of your head. You can maybe quote inflation data going back months. You probably hector your friends about what’s in the I.R.A. And hell, you probably know what I.R.A. means. I mean, what’s wrong with you? We talk a lot about the left-right divide in politics, but there’s this other divide — interested and uninterested, the people who follow politics closely and the people who avoid it as much as they can. And I think that divide is bigger, or it’s at least harder to cross. If you’re a liberal who loves MSNBC, you kind of get a conservative who loves Fox News. You have different ideas and different views. The things that are attractive to them might be repellent to you, and vice versa. But you have a similar relationship to politics and political media. But if you’re the kind of person who can’t even imagine what it would be like to not know who the Speaker of the House is, it’s hard to imagine the media habits and political thinking of someone, then, who has negative interest in Mike Johnson. But people who don’t really follow politics do vote. In 2016, about 65 percent of them said they cast a vote for president. And Trump is winning this group handily right now. There was an NBC news poll from a few months ago that found 15 percent of voters don’t follow political news, but Trump was winning them by 26 points. When you go up the scale of interest, Biden does better. Down the scale, Trump does better. Biden needs to win some of these voters back. But what drives their votes, and how do you reach them when they actively dislike and avoid political media? Yanna Krupnikov is a professor of communication and media at the University of Michigan. Along with John Barry Ryan, she is the author of “The Other Divide: Polarization and Disengagement in American Politics.” So she literally wrote the book on this. So what did she learn? As always, my email, mailto:ezrakleinshow@nytimes.com. 
# """
# translated = ChatGptTranslator(api_key='sk-proj-m24y4iL1vKwdNElI5EqpT3BlbkFJknzvJaH9lst1dLIQZbEG', target='fa').translate(text=text)
# # print(text, "@")
# print(translated)

