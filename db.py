from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["web_scraping_security"]
collection = db["scraped_data"]
