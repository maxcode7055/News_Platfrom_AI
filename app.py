from flask import Flask, render_template, request
from apps.utils.scrape import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    keyword = request.form['keyword']
    print(f"Starting scrape for keyword: {keyword}")
    scraped_data = scrape_data(keyword)
    return render_template('results.html', keyword=keyword, scraped_data=scraped_data)

if __name__ == '__main__':
    print("Starting the application...")
    app.run(debug=True)


