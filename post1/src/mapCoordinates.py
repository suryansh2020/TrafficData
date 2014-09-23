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

def find_road_name(data, pair_id, index):
    """ Find road name from parsed xml """
    return call_geocode_api(data[pair_id][index][u'lat'],
                            data[pair_id][index][u'lon'])

def request_route_info(datasource, index):
    """ Returns the nearest highway from api call

    It's called reverse geocoding and I'm a fan.
    """
    return datasource['geonames']['streetSegment'][index]['name']

def create_requests(datasource, httprequest):
    """ Create each request to geocode api """
    d = defaultdict(list)
    data = parse_xml(datasource)
    # data returns the routes, the routes plugin to the api
    for pair_id in data.keys():
        # we parse the api for highway names
        request_route_info()
        # we create a new dictionary with the highway name as the value
        d[pair_id].append()
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
    create_requests(datasource,
                    find_road_name(data, pair_id, index))

if __name__ == "__main__":
    main()

