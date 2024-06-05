from flask import Flask, render_template
from apps.utils.scrape import scrape_data 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting the application...")
    scrape_data()
    app.run(debug=True)