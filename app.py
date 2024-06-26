# from flask import Flask, jsonify, request, render_template
# from apps.utils.scrape import scrape_news
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/search_news', methods=['POST'])
# def search_news():
#     try:
#         keyword = request.form.get('q')
#         month = request.form.get('month')
#         from_day = request.form.get('from_day')
#         to_day = request.form.get('to_day')
#         year = request.form.get('year')

#         news_data = scrape_news(keyword, month, from_day, to_day, year)

#         return render_template('news_results.html', news_data=news_data)

#     except Exception as e:
#         return render_template('news_results.html', news_data=[], error=str(e))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, request, render_template
from apps.utils.scrape import scrape_news
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPEN_AI_KEY')

def translate_text_with_openai(text, target_language):
    allowed_languages = ['fa', 'es', 'fr', 'so', 'pl', 'tr', 'en']
    
    if target_language not in allowed_languages:
        return f"Error: Language '{target_language}' is not supported. Please select from {allowed_languages}."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search_news', methods=['POST'])
def search_news():
    try:
        keyword = request.form.get('q')
        month = request.form.get('month')
        from_day = request.form.get('from_day')
        to_day = request.form.get('to_day')
        year = request.form.get('year')
        language = request.form.get('language')

        news_data = scrape_news(keyword, month, from_day, to_day, year)

        translated_news_data = []
        for item in news_data:
            translated_item = item.copy()
            translated_item["title"] = translate_text_with_openai(item["title"], language)
            translated_item["full_content"] = translate_text_with_openai(item["full_content"], language) if item.get("full_content") else ""
            translated_item["source"] = translate_text_with_openai(item["source"], language) if item.get("source") else ""
            translated_item["date"] = item["date"]
            translated_item["authors"] = translate_text_with_openai(item["authors"], language) if item.get("authors") else ""
            translated_item["top_image"] = item["top_image"]
            translated_news_data.append(translated_item)

        return render_template('news_results.html', news_data=translated_news_data)

    except Exception as e:
        return render_template('news_results.html', news_data=[], error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
