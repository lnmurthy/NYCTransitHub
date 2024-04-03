from flask import Flask, jsonify

from google.protobuf.json_format import MessageToDict

from Times import Times
from Stations import Stations


app = Flask(__name__)

@app.route('/')
def landing():
  return 'welcome to NYCTransitHub backend'
 
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