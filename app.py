from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

#create endpoint get /
@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)) )