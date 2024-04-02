from flask import Flask, jsonify
from markupsafe import escape
import requests 
from google.protobuf.json_format import MessageToDict

import gtfs_realtime_pb2
import gtfs_realtime_mta_pb2

from Times import Times
from Stations import Stations


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

# @app.route('/station-info/<station>')
# def show_info(station):


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
    
@app.route('/api/train_times/')
def train_times():
  trains = Times().train_times
  return jsonify(trains)

@app.route('/api/train_times/<station_id>')
def nextTrains(station_id):
  times = Times().train_times
  station_route = list(filter(lambda station: station['station_id'] == int(station_id), times))
  station_route[0]['trains'] = list(filter(lambda train: train['time'] < 600, station_route[0]['trains']))
  
  return jsonify(station_route)

@app.route('/api/station_train_info/<station_name>')
def nextTrainsForStation(station_name):
  times = Times().train_times
  station_route = list(filter(lambda station: station['station_name'] == str(station_name), times))
  if station_route:
    station_route[0]['trains'] = list(filter(lambda train: train['time'] < 600, station_route[0]['trains']))
  
  return jsonify(station_route)

@app.route('/api/stations/')
def stops():
  stations = Stations().stations
  return jsonify(stations)