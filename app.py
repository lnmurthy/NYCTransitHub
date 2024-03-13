from flask import Flask, jsonify
from markupsafe import escape
import requests 
from google.protobuf.json_format import MessageToDict

import gtfs_realtime_pb2
import gtfs_realtime_mta_pb2

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'



@app.route("/transit")
def transit():
    #  MTA ACE Endpoint
    url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'

    
    headers = {
        'x-api-key': 'q9VMWAk6ER4dy8Dx4Skhu5McbAMWBejjan1VFQGz',
    }

    # Make the GET request
    response = requests.get(url, headers=headers, allow_redirects=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize an instance of the generated class for your protobuf data
        data = gtfs_realtime_pb2.FeedMessage()  # Replace 'YourMessageName' with the appropriate class name
        
        # Parse the binary response content into the protobuf object
        data.ParseFromString(response.content)
    
        

        return str(data.entity[0])
    
    else:
        return f"Failed to retrieve data: {response.status_code}"
