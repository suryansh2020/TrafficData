"""
Outputs a csv file (pair_id, route)

This includes the logic for deciding the correct road when using
reverse geocoding. 
"""
from collections import defaultdict
import xmltodict
from checkPairId import datasources

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
    
def request_route_info(datasource):
    """ Makes a call to the api and returns the nearest highway

    It's called reverse geocoding and I'm a fan.
    """
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

