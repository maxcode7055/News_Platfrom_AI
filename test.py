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





# import os
# from dotenv import load_dotenv
# from deep_translator import ChatGptTranslator

# load_dotenv()

# text = """
# Yanna Krupnikov probes the motivations of Americans who avoid politics — but often vote. ezra kleinFrom New York Times Opinion, this is “The Ezra Klein Show.” If you are listening to this show, you’re an odd duck. I mean, I’m an odd duck, too. But if you’re here, you can probably, say, list the Trump trials off the top of your head. You can maybe quote inflation data going back months. You probably hector your friends about what’s in the I.R.A. And hell, you probably know what I.R.A. means. I mean, what’s wrong with you? We talk a lot about the left-right divide in politics, but there’s this other divide — interested and uninterested, the people who follow politics closely and the people who avoid it as much as they can. And I think that divide is bigger, or it’s at least harder to cross. If you’re a liberal who loves MSNBC, you kind of get a conservative who loves Fox News. You have different ideas and different views. The things that are attractive to them might be repellent to you, and vice versa. But you have a similar relationship to politics and political media. But if you’re the kind of person who can’t even imagine what it would be like to not know who the Speaker of the House is, it’s hard to imagine the media habits and political thinking of someone, then, who has negative interest in Mike Johnson. But people who don’t really follow politics do vote. In 2016, about 65 percent of them said they cast a vote for president. And Trump is winning this group handily right now. There was an NBC news poll from a few months ago that found 15 percent of voters don’t follow political news, but Trump was winning them by 26 points. When you go up the scale of interest, Biden does better. Down the scale, Trump does better. Biden needs to win some of these voters back. But what drives their votes, and how do you reach them when they actively dislike and avoid political media? Yanna Krupnikov is a professor of communication and media at the University of Michigan. Along with John Barry Ryan, she is the author of “The Other Divide: Polarization and Disengagement in American Politics.” So she literally wrote the book on this. So what did she learn? As always, my email, mailto:ezrakleinshow@nytimes.com. 
# """
# translated = ChatGptTranslator(api_key=os.getenv('OPEN_AI_KEY'), target='fa').translate(text=text)
# # print(text, "@")
# print(translated)


import os
from dotenv import load_dotenv
from deep_translator import ChatGptTranslator

load_dotenv()

text = """
The battle for Gen Z social shoppers
Date: 2024-06-14

Source: BBC

Full Content:

Shopping habits have not been the same since the Covid pandemic and resulting lockdowns. For many, and particularly younger shoppers,... The battle for Gen Z social shoppers 7 days ago Lilia Souri and AJ Pulvirenti - hosts of the podcast Gen Z on Gen Z Shopping habits have not been the same since the Covid pandemic and resulting lockdowns. For many, and particularly younger shoppers, it saw the lines blur between social media and e-commerce. Unable to shop in person, and with TikTok downloads soaring, a trend began that would go on to be described as a cultural phenomenon: #TikTokMadeMeBuyIt. The hashtag, where users post what they’ve bought thanks to recommendations about products on the app, has now been posted more than seven billion times. For Lilia Souri and AJ Pulvirenti who co-host the marketing podcast "Gen Z on Gen Z" by creative agency Movers+Shakers, TikTok is winning with their generation. "It’s become one of the biggest because of how advanced the algorithm is, and because, before TikTok Shop even was created, we were seeing shopping behaviours happening on TikTok as a whole,” says 27-year-old Lilia Souri. “You can purchase a product directly on the platform, and then continue scrolling, in a cycle of watch, shop, repeat,” her co-host AJ Pulvirenti, 25, adds. Social shopping is a big market and growing fast. In 2023 globally it was worth $570bn (£446bn), and is forecast to be worth more than a trillion dollars by 2028, . While TikTok is one of the big players, its position looks vulnerable. TikTok unless it is sold by its Chinese parent company ByteDance. So where would that leave social shopping? If you look at the number of buyers, then Facebook is still the biggest presence in social shopping, according to Jasmine Enberg, chief social media analyst at E Marketer. Most of its transactions take place on Facebook Marketplace, “one of the few places where Gen-Z and young people still go to on Facebook,” she adds. But if you're looking at the percentage of users who actually buy something, then TikTok is ahead, says Ms Enberg. Data from US-based E-marketer suggests 40% of TikTok users in the US will make at least one purchase on the platform this year, in front of both Facebook and Instagram. “It’s a very important activity on the app, especially for its users,” says Ms Enberg. Keen not to be left out, Amazon added a Consult-a-Friend feature last year, allowing customers to ask friends for advice while scrolling through its app. Gen Z podcaster AJ Pulvirenti is sceptical about these new features. “When a platform just tries to replicate something from another platform and doesn't offer anything very new or intriguing about it, it's not going to make people feel inclined to switch from something that they're used to,” he says. A recent study by market-research firm Data.ai suggests that Gen Z spend around two hours a day on TikTok, compared to a little less than 10 minutes on Amazon. Livestream seller Evo Syah built a successful business on social shopping Perhaps TikTok's experience in Indonesia might have some useful lessons. In 2021 it became the first country to pilot the app's e-commerce service, and became one of the biggest markets for TikTok Shop. But with local commerce suffering in the wake of the pandemic, the government introduced rules last October to protect local retailers, which forced TikTok Shop to close. For 26-year-old entrepreneur Evo Syah it was a major blow. “It’s hard for me, but what I can do?” he says recalling the tough decisions he had to make. “I just start my business for one year, and then they shut me down,” he says. But two months after the closure, TikTok agreed to invest $1.5bn in Indonesia’s biggest e-commerce platform Tokopedia, meaning sellers like Evo Syah and millions of others could return to the app. The 26-year-old said he “never felt happier”. But not everything went back to normal. "Before the TikTok shop closed I could get sales like 20 million rupiah (£966) daily. But after it reopened again that’s down to 10 million rupiah (£483),” he says. Mr Syah sells most of his products on livestreams, a selling method which has boomed in popularity in Asia, but according to Ms Enberg has failed to take off in the UK and US. “Indonesia is a very different commerce landscape to the US,” she says. However, in both Indonesia and the US, TikTok Shop has been crucial for a lot of small and local merchants, she adds. “Many of them don't really have another place that is as powerful as TikTok.” Indonesia was a big market for TikTok Shop with livestreamers like Monomolly
"""

def translate_text(text, target_languages):
    translations = {}
    api_key = os.getenv('OPEN_AI_KEY')
    
    for lang in target_languages:
        translator = ChatGptTranslator(api_key=api_key, target=lang)
        translations[lang] = translator.translate(text=text)
    
    return translations

# target_languages = ['fa', 'es', 'fr', 'so', 'pl', 'tr', 'en']  # Persian, Spanish, French
target_languages = ['so', 'es']  # Persian, Spanish, French

translated_texts = translate_text(text, target_languages)

for lang, translation in translated_texts.items():
    print(f"Translation in {lang}:")
    print(translation)
    print("\n")
