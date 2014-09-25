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

def http_request(requests, data, pair_id, index):
    """ Sanity inducing, need to know which functions are making the
    http request.

    Args:
        requests: list, int, indexed position of roads you want to be
                  returned. If you want just the nearest road then you'd
                  want [0].
        data: dict, pair_id mapped onto an ordered_dict of coordinates
        pair_id: key value from the data parameter
        index: int, iterator that chooses coordinate pairs
    Returns:
        List, str; list of closest streets/highways to the coordinates
        given 
    """
    # Dictionary of parsed xml from the geocode api
    data = find_road_name(data, pair_id, index)
    # nearest highways to given coordinates; using reverse geocoding
    routes = []
    # parses out closest roads depending on the index value of requests
    while requests:
        routes.append(request_route_info(data, requests.pop()))
    return routes

def generate_request(datasource):
    """ Since we're not using twisted, things are getting ugly

    Args:
        datasource:
    Returns:
        str, item from datasource.keys() OR returns False if no
        more items in datasource.keys().
    """
    data = datasource.keys()
    try:
        while data:
            yield data.pop()
    except StopIteration:
        return False

def create_requests(datasource, http_request):
    """ Create each request to geocode api
    
    Args:
        datasource: dict, pair_routes.xml converted via open_xml()
        httprequest: http_request(requests, data, pair_id, index)
    Returns:
        default dict (list), where pair id is mapped to nearests roads
    """
    d = defaultdict(list)
    data = parse_xml(datasource)
    # data returns the routes, the routes plugin to the api
    while http_request:
        # iterate through each pair_id when an http_request arrives
        pair_id = generate_request(datasource).next()
        if pair_id == False:
            break
        # we parse the api for highway names
        # we create a new dictionary with the highway name as the value
        d[pair_id].append(http_request.pop())
    yield d

# this is fucked. It might be better to redo this using twisted.
# Async wins again.

def decide_nearest_highway(datasource):
    """ Decide which highway is closest to each pair_id """
    find_road_name(data, pair_id, index)
        
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

