""" Parsing the descriptions of locations given in pair_routes.xml

An 'Origin' and a 'Destination' string is given for each pair_id in
pair_routes.xml. Given the trouble with using reverse geocoding to
identify highway locations, parsing these descriptions may be the
part of the best approach. At the end of the day, a mixed strategy
may prevail.

Each highway is identified using rules that we can identify within
the text.

Here's the rules:
1) Each string mentions the highway first.
2) Some strings include a space in the highway name like Rt. 3

That's it. Tokenizing each string based on spaces then popping off
the first item in each queue.
"""
import re
import time
import logging
from collections import deque

from mapCoordinates import open_xml, parse_pair_id
from checkPairId import enable_log


# for each pair_id in pair_routes.xml, return the 'Origin' and the
# 'Destination' tags.
def parse_tags(datasource, count):
    """ Parse 'Origin' and 'Destination' for each pair_id

    Args:
        datasource: pair_routes.xml converted to a dict via open_xml()
    Returns:
        tuple, unicode, ('Origin', 'Destination')
    """
    origin = datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA']\
             [count][u'Origin']
    destination = datasource[u'btdata'][u'TRAVELDATA'][u'PAIRDATA']\
             [count][u'Destination']
    return (origin, destination)

# parse & pop
def parse_and_pop(string):
    """ Parse the highway name that's being described

    Args:
        string: unicode, 'Origin' or 'Destination'
    Returns:
        str, name of a highway that's being described
    """
    pattern = re.compile("\w{2,3}[.] \d{3}?|\w{2,3}[.] \d{1,3}?|"+\
                         "\w{2,3} \d{3}?|\w{2,3} \d{1,3}?|"+\
                         "\w-\d{3}?|\w-\d{2}?|\d{2,3}?")
    if pattern.search(string):
        return pattern.search(string).group()
    else:
        return deque(string.split(" ")).popleft()

def lookup_pairs(datasource):
    """ Create data structure from parsed pair_routes.xml """
    lookup_dict = {}
    count = 0
    start = time.time()
    while count < len(parse_pair_id(datasource)):
        lookup_dict[parse_pair_id(datasource)[count]\
            [u'PairID']] = parse_tags(datasource, count)
        count += 1
    # logging loops
    logging.info("Time elapsed for lookup_pairs parse: "+\
                 str(time.time() - start))
    return lookup_dict

def whitelist():
    """ List of highway names that are acceptable """
    logging.info("Whitelist called")
    return []
    
# classify 'intersectors', 'singulars', and 'others'
def classify_pairs(datasource, whitelist):
    """ Classify each pair_id so it can be further processed

    Classifications:
        'intersectors': 'origin' and 'destination' are the same highway
        'disjointers': 'origin' and 'destination' are different roads
        'others': either 'origin' or 'destination' are not a highway

    Args:
        datasource: dict, lookup_pairs(datasource)

    Returns:
        dictionary or something like that.
    """
    # timing
    start = time.time()
    # Classifications
    intersectors = []
    disjointers = []
    others = []
    # Sorting
    for pair_id in datasource:
        logging.info("Parsing pair_id: "+str(pair_id))
        origin, destination = datasource[pair_id]
        origin = parse_and_pop(origin)
        destination = parse_and_pop(destination)
        
        #if origin not in whitelist or destination not in whitelist:
            #others.append(pair_id)
            #pass
        if origin == destination:
            intersectors.append(pair_id)

        else:
            disjointers.append(pair_id)
            logging.warning("Disjointers: "+str(origin)+\
                            " and "+str(destination))

            
    logging.info("Time elapsed for pair classification: "+\
                 str(time.time() - start))
    return (others, intersectors, disjointers)
    # need to add logging & tests

def metrics(datasource, whitelist):
    """ Logging some metrics on the parse """
    others, intersectors, \
        disjointers = classify_pairs(datasource, whitelist)
    logging.info("Others: "+str(len(others)))
    logging.info("Intersectors: "+str(len(intersectors)))
    logging.info("Disjointers: "+str(len(disjointers)))
    logging.info("Total: "+str(len(others)+len(intersectors)+\
                               len(disjointers)))

def main():
    logging.info("START - Beginning the parse")
    metrics(lookup_pairs(open_xml()), whitelist())

if __name__ == "__main__":
    enable_log("highwayParser")
    main()
