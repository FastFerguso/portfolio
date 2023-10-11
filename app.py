import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request, render_template
from pymongo import MongoClient
import ssl

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI, ssl_cert_reqs=ssl.CERT_NONE)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
   return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
   return render_template('about.html')

@app.route('/info', methods=['POST'])
def test_post():
    full_name = request.form['full_name']
    email = request.form['email']
    message = request.form['message']

    data = {
        'full_name': full_name,
        'email': email,
        'message': message
    }

    db.message.insert_one(data)

    return 'Thanks for the message!'

if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)