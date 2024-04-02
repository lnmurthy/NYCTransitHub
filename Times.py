import time
from itertools import chain

from feed_generator import FeedGenerator

from utils import get_updates, get_route_id
from Stations import Stations

MAX_TIME_DIFFERENCE = 1800

class Times:
  def __init__(self):
    self.feed = FeedGenerator().feed
    self.train_times = self.get_times()
  
  def process_update(self, entity, update, times):
    time_difference = self.get_time_difference(update)
    stopId = update['stopId'][:-1]
    if time_difference != None and time_difference > 0 and time_difference < MAX_TIME_DIFFERENCE:
      # add direction to route id 
      # Direction is the last character 'N' or 'S' at the end of the stop Id
      route_id = get_route_id(entity) 
      direction = update['stopId'][-1]
      times.append({'stop_id': stopId, 'route_id': route_id, 'direction': direction, 'time':time_difference})
    return times
  
  def process_entity(self, entity, times):
    if 'tripUpdate' in entity.keys() and "stopTimeUpdate" in entity['tripUpdate'].keys(): 
      updates = get_updates(entity)
      for update in updates:
        times = self.process_update(entity, update, times)
    return times

  def get_times(self):
    times = []
    for entity in self.feed:
      times = self.process_entity(entity, times)
    #times = list(chain.from_iterable(times))
    station_times = self.get_station_times(times)
    return station_times
  
  def get_station_times(self, times):
    station_times = []
    stations = Stations().stations
    for station in stations:
      stations_dict = {'station_id': station['station_id'], 'station_name': station['name'], 'trains': []}
      for stopId in station['stop_ids']:
        stop_times = list(filter(lambda time: time['stop_id'] == stopId, times))
        for time in stop_times:
          stations_dict['trains'].append(time)
      stations_dict['trains'] = sorted(stations_dict['trains'], key = lambda i: i['time'])
      station_times.append(stations_dict)
    return station_times

  @staticmethod
  def get_time_difference(update):
    """Return time difference between current time and train arrival/departure time in seconds"""
    if "arrival" in update.keys() and "time" in update["arrival"].keys():
      # time in gtfs feed is in POSIX
      return float(update["arrival"]["time"]) - time.time()
    elif "departure" in update.keys() and "time" in update["departure"].keys():
      return float(update["departure"]["time"]) - time.time()
    else: return None
