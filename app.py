import os
from flask import Flask
from routes import pages #routes.py file import pages blueprint
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() # import all .env variables from our hidden file (dot = .), or if we are on render.com via a separate file called .env.

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI")) #or this option:  os.environ.get("MONGODB_URI")
    app.db = client.RodgeHabz
    
    app.register_blueprint(pages)
    return app
