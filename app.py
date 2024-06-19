from flask import Flask, jsonify, request, render_template
from apps.utils.scrape import scrape_news
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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

        news_data = scrape_news(keyword, month, from_day, to_day, year)

        return render_template('news_results.html', news_data=news_data)

    except Exception as e:
        return render_template('news_results.html', news_data=[], error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
