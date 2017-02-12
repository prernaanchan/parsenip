import os
import datetime
from flask import Flask
from flask import jsonify, request, json
from git import Repo


flock_key = None
flock_secret = None
flock_url = None

try:
    with open('config.json') as data_file:    
        data = json.load(data_file)
    # flock creds
    flock_key = data['flock_key']
    flock_secret = data['flock_key']
    flock_url = data['flock_url']

except IOError as e:
      print "[error] "+e.message


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