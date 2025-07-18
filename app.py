from flask import Flask, request, jsonify, render_template
from db import collection
from scraper import scrape_website

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = scrape_website(url)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    # Save or update the scan result in MongoDB
    collection.update_one({"url": url}, {"$set": result}, upsert=True)

    return jsonify(result)

@app.route('/result')
def result():
    url = request.args.get('url')
    if not url:
        return "URL parameter is required", 400

    record = collection.find_one({"url": url}, {"_id": 0})
    if not record:
        return "Result not found", 404

    return render_template('result.html', result=record)

@app.route('/result_data')
def result_data():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    record = collection.find_one({"url": url}, {"_id": 0})
    if not record:
        return jsonify({"error": "Result not found"}), 404

    return jsonify(record)

if __name__ == '__main__':
    app.run(debug=True)
