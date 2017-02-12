import os
import datetime
from flask import Flask
from flask import jsonify, request, json
from git import Repo


#Create an instance of flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return 'Hello World'
@app.route('/process', methods=['POST'])
def process():
    resp = request.data
    data =  json.loads(resp)
    if data.has_key('text'):
        if data['text'].lower() == 'deploy':
            # Git Clone Project
            # Run the Check against the HAR file
            # On Error post back to Flock with error
    print data
    return jsonify(data)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=5000)