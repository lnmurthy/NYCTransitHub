from datetime import date


def get_route_id(entity):
  # get route id to get info on where the train is going
  return entity["tripUpdate"]["trip"]["routeId"]

def get_updates(entity):
  updates = entity["tripUpdate"]["stopTimeUpdate"]
  return updates