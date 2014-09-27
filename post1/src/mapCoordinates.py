"""
Outputs a csv file (pair_id, route)

This includes the logic for deciding the correct road when using
reverse geocoding. 
"""
# get pair id from pair_routes.xml, get route coordinates
# check two coordinate pairs per pair_id with geocode api
# return nearest road for each coordinate pair
# pair_id mapped to nearest two roads for each coordinate pair
# write to csv
import sys
import io
import json
import logging
from collections import defaultdict

import requests # can't justify using twisted getPage :(
import xmltodict

from checkPairId import datasources
from secret import username

# get pair id from pair_routes.xml, get route coordinates
def open_xml():
    """ Opens pair_routes.xml and returns a dictionary """
    gb1,gb2,pair_routes = datasources()
    with open(pair_routes) as fd:
        obj = xmltodict.parse(fd.read())
    return obj
    
def parse_pair_id(datasource):
    """ Returns each pair ID

    Args:
        datasource: pair_routes.xml converted to a dictionary
                    via open_xml()
    Returns:
        List, each item is a pair ID. Drills down into the dictionary
        to pull this out.
    """
    return datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA']

def parse_routes(datasource, count):
    """ Returns each child of routes where pair ID is the parent

    Args:
        datasource: dict, pair_routes.xml converted via open_xml()
        count: int, iterator for each route associated with a pair_id
    Returns:
        Ordered dict of coordinates as values for a dict mapped to
        each pair_id
    """
    return datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA'][count]\
        [u'Routes'][u'Route']
    
def parse_xml(datasource):
    """ Retrieve items from xml
    
    Args:
        datasource: dict, pair_routes.xml converted via open_xml()
    Returns:
        default dict, list; pair_id is mapped onto a list of ordered
        dictionaries with two items. 'lat' and 'lon' as keys mapped
        onto their coordinate values. 
    """
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
    """ Find road name from parsed xml

    Args:
        data: dict, pair_id mapped onto an ordered_dict of coordinates
        pair_id: key value from the data parameter
        index: int, iterator that chooses coordinate pairs
    Returns:
        Dictionary of parsed xml from the geocode api
    """
    return call_geocode_api(data[pair_id][index][u'lat'],
                            data[pair_id][index][u'lon'])

def http_request(requests, datasource):
    """ Sanity inducing, need to know which functions are making the
    http request.

    Args:
        requests: list, int, indexed position of roads you want to be
                  returned. If you want just the nearest road then
                  you'd want [0].
        datasource: find_road_name(data, pair_id, index)
    Returns:
        List, str; list of closest streets/highways to the coordinates
        given 
    """
    # Dictionary of parsed xml from the geocode api
    data = datasource
    # nearest highways to given coordinates; using reverse geocoding
    routes = []
    # parses out closest roads depending on the index value of requests
    while requests:
        routes.append(request_route_info(data, requests.pop()))
    return routes

def create_requests(datasource, http_request):
    """ Create each request to geocode api
    
    Args:
        datasource: dict, pair_routes.xml converted using parse_xml()
        httprequest: http_request(requests, data, pair_id, index)
    Returns:
        default dict (list), where pair id is mapped to nearests roads
    """
    for pair_id in datasource.keys():

        data = http_request[pair_id]
        while data:
            d[pair_id].append(data.pop())
    return d

def request_route_info(datasource, index):
    """ Returns the nearest highway from api call

    It's called reverse geocoding and I'm a fan.
    Args:
       datasource: dict, xml to dictionary for request of geonames api
       index: int, iterator for choosing nearby streets
    Returns:
       str, name of nearest street/highway
    """
    return datasource['geonames']['streetSegment'][index]['name']

def street_suggestions(datasource):
    """ Return street suggestions from geocode api

    Args:
        datasource: pass
    Returns:
        List, str, closest road to a set of coordinates.
    """
    count = 0
    nearest_roads = []
    while count < len(datasource['geonames']['streetSegment']):
        nearest_roads.append(request_route_info(datasource, count))
        count += 1
    return nearest_roads
    
# check two coordinate pairs per pair_id with geocode api
def request_nearest_road(datasource):
    """ Requests nears road to coordinate pair from a route

    Args:
        datasource: pair_routes.xml converted to a dictionary
                    via open_xml()

    Calls a bunch of functions:
        parse_xml(datasource): returns pair_id and routes from
                               pair_routes.xml
        find_road_name(data, pair_id, index): returns results from
                               the geocode api as a dictionary for
                               each coordinate pair as params.
        request_route_info(datasource, index): returns str, name of
                               nearest highway to coordinate pair.

    Returns:
        pair_id mapped to a list of nearest highways to the first and
        last coordinate pair given as its route from pair_id.xml
    """
    # returns dictionary with pair_id mapped to route coordinates
    d = defaultdict(list)
    # call two coordinate pairs from each route mapped to pair_id
    data = parse_xml(datasource)
    count = 0
    for pair_id in data.keys():
        # return two coordinate pairs
        count += 1
        print count, " out of ", len(data.keys()), " requested"
        # send each coordinate pair to the geocode api
        pair1 = find_road_name(data, pair_id, 0)
        pair2 = find_road_name(data, pair_id, -1)

        # parse contents from api to get route names
        nearest_road1 = street_suggestions(pair1)
        nearest_road2 = street_suggestions(pair2)

        # append nearest roads for each pair_id
        d[pair_id].append((nearest_road1, nearest_road2))
    return d

def output_to_json(datasource):
    """ Outputs geocode results to JSON """
    # needs to support utf-8
    with io.open("geocode.txt", 'w', encoding="utf-8") as f:
        f.write(unicode(json.dumps(datasource, ensure_ascii=False)))
    f.close()
   
def main():
    """ Main function for program """
    output_to_json(request_nearest_road(open_xml()))

if __name__ == "__main__":
    main()



