"""
Outputs a csv file (pair_id, route)

This includes the logic for deciding the correct road when using
reverse geocoding. 
"""
from collections import defaultdict
import xmltodict
import sys
import requests # can't justify using twisted getPage :(

from checkPairId import datasources
from secret import username

def open_xml():
    gb1,gb2,pair_routes = datasources()
    with open(pair_routes) as fd:
        obj = xmltodict.parse(fd.read())
    return obj
    
def parse_pair_id(datasource):
    """ Returns each pair ID
    """
    return datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA']

def parse_routes(datasource, count):
    """ Returns each child of routes where pair ID is the parent
    """
    return datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA'][count]\
        [u'Routes'][u'Route']
    
def parse_xml(datasource):
    """ Retrieve items from xml """
    d = defaultdict(list)
    count = 0
    while count < len(parse_pair_id(datasource)):
        pair_id = parse_pair_id(datasource)[count][u'PairID']
        for route in parse_routes(datasource, count):
            d[pair_id].append(route)
        count += 1
    return d

def make_geocode_api(lat, lon):
    """ Creates a call for the api """
    base = "http://api.geonames.org/findNearbyStreets?"
    latitude = "lat=" + lat
    longitude = "&lng=" + lon
    user = "&username=" + username
    return base+latitude+longitude+user
    
def call_geocode_api(lat, lon):
    """ Calls the api """
    r = requests.get(make_geocode_api(lat, lon))
    return xmltodict.parse(r.text)
    
def request_route_info(datasource, index):
    """ Returns the nearest highway from api call

    It's called reverse geocoding and I'm a fan.
    """
    return datasource['geonames']['streetSegment'][index]['name']

def find_road_name(data, pair_id, index):
    """ Find road name from parsed xml """
    return call_geocode_api(data[pair_id][index][u'lat'],
                            data[pair_id][index][u'lon'])

def create_requests(datasource, httprequest):
    """ Create each request to geocode api """
    d = defaultdict(list)
    data = parse_xml(datasource)
    for pair_id in data:
        # call the first & last coordinates. Pretty sure
        # we shouldn't have problems with routes intersecting;
        # it could happen. Let's see how it goes.
        first = find_road_name(data, pair_id, 0) # this code is twisted,
        # take a break
        last = find_road_name(data, pair_id, -1)
        # parse out the dictionaries to return the road names
        d[pair_id].append(request_route_info(first, 0))
        # append the nearest highways of the first and last
        # coordinates to the defaultdict
    return d

def decide_nearest_highway(datasource):
    """ Decide which highway is closest to each pair_id """
    pass
        
def write_csv_file(datasource):
    """ Output, (pair_id, Route)
    """
    pass

def main():
    """ Main function for program """
    datasource = open_xml()

if __name__ == "__main__":
    main()

