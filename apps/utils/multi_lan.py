# from transformers import MBartForConditionalGeneration, MBart50Tokenizer

# def download_model():
#     model_name = "facebook/mbart-large-50-many-to-many-mmt"
#     model = MBartForConditionalGeneration.from_pretrained(model_name)
#     tokenizer = MBart50Tokenizer.from_pretrained(model_name)
#     return model, tokenizer

# def translate_text(text, model, tokenizer, target_lang):
#     tokenizer.src_lang = "en_XX"  # English
#     tokenizer.tgt_lang = target_lang  # Target language
#     encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
#     out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
#     return out

# model, tokenizer = download_model()

# # Example text to be translated
# text = input("Enter Your Text for translation...")

# english_text = f"""{text}"""

# # Define the target languages
# languages = {
#     "English": "en_XX",
#     "Farsi (Persian)": "fa_IR",
#     "French": "fr_XX",
#     "Polish": "pl_PL",
#     "Somali": "so_SO",
#     "Spanish": "es_XX",
#     "Turkish": "tr_TR"
# }

# # Translate text to each language and print the result
# for lang, lang_code in languages.items():
#     translated_text = translate_text(english_text, model, tokenizer, lang_code)
#     print(f"Translation in {lang}:\n{translated_text[0]}\n")

# import serpapi
# from pprint import pprint
# from bs4 import BeautifulSoup

# def news(soup, url_to_scrape):
#     try:
#         client = serpapi.Client(
#             api_key="31b31eafbec0aedaaf48e8ebf8d2baa55faff180c67ae66e95007895ddc560c1")

#         resultss = client.search({
#             "engine": "google_news",
#             "q": "India election",
#             "include_html": True 
#         })

#         newsresults = resultss.get("news_results", [])
#         print(newsresults,"/"*80)    

#         news_data_list = []
#         max_news_items = 6
#         news_counter = 0

#         for result in newsresults:
#             if news_counter >= max_news_items:
#                 break

#             title = result.get("title", "")
#             link = result.get("link", "")
#             date = result.get("date", "")
#             source = result.get("source", {})
#             name = source.get("name", "")
#             icon = source.get("icon", "")
#             authors = ", ".join(source.get("authors", [])) if source.get("authors") else ""
#             thumbnail = result.get("thumbnail", "")
            
#             # Initialize description with an empty string
#             description = ""
#             # Try to extract from different fields
#             for field in ["description", "snippet", "abstract", "summary", "content", "body", "article"]:
#                 # print("in loop")
#                 if result.get(field):
#                     description = result[field]
#                     print(result[field],"*"*80)
#                     break

#             # If HTML content is available, extract text from <div> and <p> tags
#             html_content = result.get("html", "")
#             if html_content:
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 div_text = soup.find('div')
#                 p_text = soup.find('p')
#                 if div_text:
#                     description += "\n" + div_text.get_text(separator="\n").strip()
#                 if p_text:
#                     description += "\n" + p_text.get_text(separator="\n").strip()

#             news_item = {
#                 "title": title,
#                 "link": link,
#                 "date": date,
#                 "source_name": name,
#                 "source_icon": icon,
#                 "authors": authors,
#                 "thumbnail": thumbnail,
#                 "description": description.strip(),  # Strip leading/trailing whitespace
#             }

#             news_data_list.append(news_item)
#             news_counter += 1

#         return news_data_list

#     except Exception as e:
#         response_data = {
#             "status": 400,
#             "message": f"Error: {str(e)}",
#             "data": []
#         }
#         return response_data

# if __name__ == "__main__":
#     results = news(soup=None, url_to_scrape=None)
#     pprint(results)


import torch
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
from langdetect import detect
from flask import Flask, jsonify, request
from serpapi import GoogleSearch
from datetime import date
from bs4 import BeautifulSoup
import requests
import re
import asyncio
import aiohttp

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def load_model(pretrained_model: str = "facebook/m2m100_1.2B"):
    tokenizer = M2M100Tokenizer.from_pretrained(pretrained_model)
    model = M2M100ForConditionalGeneration.from_pretrained(pretrained_model).to(device)
    return model, tokenizer

model, tokenizer = load_model()

app = Flask(__name__)

def format_date(month, day, year):
    return f"{month}/{day}/{year}" if month and day and year else ""

def clean_text(text):
    cleaned_text = re.sub(r'[\\→\n\"/]', '', text)
    return cleaned_text.strip()

async def translate_text_async(text, model, tokenizer, src_lang, target_lang, max_length=10240):
    tokenizer.src_lang = src_lang
    encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.get_lang_id(target_lang),
        max_length=max_length,
    )
    out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return out
def translate_text(text, model, tokenizer, target_lang):
    tokenizer.src_lang = "en_XX"  
    tokenizer.tgt_lang = target_lang 

    if target_lang in tokenizer.lang_code_to_id:
        encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        generated_tokens = model.generate(
            **encoded_text,
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
        )

        out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return out
    else:
        return ["Translation not available for this language code."]

@app.route('/search_news', methods=['POST'])
async def search_news():
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

        text = input("Enter Your Text for translation...")

        params = {
            "q": keyword,
            "tbm": "nws",
            "num": "2",
            "tbs": tbs_param,
            "api_key": "93eed08042f625c377626ad343660e93aececc16f411a0aa2667840d201ea910"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]

        tasks = []
        for result in news_results:
            tasks.append(fetch_and_translate(result["link"], result.get("snippet", ""), detect(result.get("snippet", ""))))
        languages = {
            "English": "en_XX",
            "Farsi (Persian)": "fa_IR",
            "French": "fr_XX",
            "Polish": "pl_PL",
            "Somali": "so_SO",
            "Spanish": "es_XX",
            "Turkish": "tr_TR"
        }

        for lang, lang_code in languages.items():
            translated_text = translate_text(english_text, model, tokenizer, lang_code)
            print(f"Translation in {lang}:\n{translated_text[0]}\n")

            translated_news_items = await asyncio.gather(*tasks)

            return jsonify(translated_news_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def fetch_and_translate(url, snippet, src_lang):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")

                for unwanted in soup(['header', 'footer', 'nav', 'a', 'strong', 'span', 'i', 'script', 'style']):
                    unwanted.decompose()

                paragraphs = soup.find_all("p")
                full_content = ""
                for para in paragraphs:
                    para_text = para.get_text().strip()
                    if para_text:
                        full_content += para_text + " "
                full_content = clean_text(full_content)

                async with aiohttp.ClientSession() as session_translate:
                    tasks_translate = []
                    for lang, lang_code in languages.items():
                        tasks_translate.append(translate_text_async(full_content, model, tokenizer, src_lang, lang_code))
                    
                    translated_texts = await asyncio.gather(*tasks_translate)
                    
                    translations = {}
                    for i, (lang, lang_code) in enumerate(languages.items()):
                        translations[lang] = translated_texts[i][0]

                    return {
                        "snippet": clean_text(snippet),
                        "full_content": full_content,
                        "translations": translations
                    }

            else:
                return {
                    "snippet": f"Failed to fetch article content: {response.status}",
                    "full_content": "",
                    "translations": {}
                }

    except Exception as e:
        return {
            "snippet": f"Error fetching article content: {str(e)}",
            "full_content": "",
            "translations": {}
        }

if __name__ == '__main__':
    languages = {
        "English": "en",
        "Spanish": "es",
        "Persian": "fa",
        "French": "fr",
        "Polish": "pl",
        "Somali": "so",
        "Turkish": "tr"
    }
    app.run(debug=True)