# app.py
from flask import Flask, render_template, jsonify
from scrapper.selenium_scapper import TwitterTrendsScraper
from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    try:
        scraper = TwitterTrendsScraper()
        result = scraper.scrape()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-latest')
def get_latest():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Get the most recent record
        latest_record = collection.find_one(
            sort=[("timestamp", -1)]
        )
        
        if latest_record:
            # Convert ObjectId to string for JSON serialization
            latest_record['_id'] = str(latest_record['_id'])
            return jsonify(latest_record)
        else:
            return jsonify({"error": "No records found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)