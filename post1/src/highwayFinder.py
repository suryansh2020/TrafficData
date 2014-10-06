# going to try a different approach in highwayParser.py
""" Figuring out which coordinates map to which roads

The goal is to find a consensus between pair_definitions.csv and
the reverse geocoding api from geocache. Both approaches were used
because each approach includes incomplete information.

For example, 'pair_id' '10599' gives a 'Description' for the location
as '6WB-MM055.9'.

However, most descriptions are something like 'I-90 WB after on-ramp
(Newton Corner)'. Pretty helpful, we can parse some things out with
regular expressions and reasonably conclude that this point is located
on 'I-90'. When we plug in the pair_id, '10498', to the geocode api,
we find that 'I-90', is also returned.

It's also important to know that Ids don't match across the three
datasources we have available. There's not much we can do about it.
The solution is to just use what's in the xml as the point of
departure. Otherwise, we have no way of attaching coordinates to
the data. We should just acknowledge these data points as 'dead'
and have a funeral.
"""
import os
import io
import re
import csv
import json
import time
import logging
from collections import Counter, deque

from checkPairId import datasources, enable_log

def read_json():
    """ Reading in json data from geocode api 

    json data is based on pair_routes.xml

    Bypassing tests that the user is in the correct directory because
    they should have figured it out by now.
    """
    da_path = os.path.abspath("")+ "/post1/src/geocode.txt"
    # needs to support utf-8
    with io.open(da_path, 'r', encoding="utf-8") as f:
        logging.info("Read json file into memory")
        return json.load(f)

def use_correct_csv_column(datasource):
    """ Let's make sure we're grabbing the correct columns
    
    Returns:
        Tuple, pair_id, Description from pair_definitions.csv
    """
    logging.info("Indexed row for reading csv file")
    return (datasource.index("pair_id"),
            datasource.index("Description"))
    
def read_description(datasources):
    """ Returns pair_id mapped to description
    from pair_definitions.csv"""
    # timing function
    start = time.time()
    # path to data
    junk, datasource, junk = datasources
    pair_definitions = {}
    with open(datasource, 'rb') as f:
        header = True
        reader = csv.reader(f, delimiter = ",")
        # attempt to return a list of strings, where each string
        # is a pairID
        try:
            for row in reader:
                if header == True:
                    logging.info("Read in header of csv")
                    pair_id, definition = use_correct_csv_column(row)
                    header = False
                else:
                    pair_definitions[row[pair_id]]=row[definition]
        except csv.Error as e:
            logging.critical('datasource %s, line %d: %s' %
                             (datasource, reader.line_num, e))
    logging.info("Elapsed time for parse: " + str(time.time() - start))
    return pair_definitions

def parse_description(datasource):
    """ Just don't try to regex pair_definitions.csv. It's a mess.
    Compare the reverse geocoding to the descriptions given but like
    don't go down this road. Life is too short. """
    pass

def nearest_highway(geocode_json):
    """ Compare most often listed highways for coordinate pairs

    This approach is only returning an 'agreed upon' location for 62
    out of 155 pair_id's (40%). We're going to have to try some
    different approaches.
    
    Args:
        geocode_json: Geocode api written to json; can be accessed
                      using read_json()
    Returns:
        Dict, str, pair_id mapped onto the nearest highway
    """
    logging.info("STARTED - Nearest highway comparisons")
    # Used for matches/total
    total = 0
    agreement = 0
    
    for pair_id in geocode_json.keys():
        
        # Used for matching
        count = 0
        first = True
        agree = "None"
        logging.info("Using pair_id: "+ str(pair_id))
        while count < len(geocode_json[pair_id][0]):
            
            c = Counter(geocode_json[pair_id][0][count])
            road, num = c.most_common(1)[0]
            logging.info(road)
            if first:
                logging.info("Set first most common road to itself")
                agree = road
                first = False
                
            elif road != agree:
                logging.info("Using list number: " + str(count))
                logging.critical(str(agree) + " is not equal to " +\
                                 str(road))
                
            elif road == agree:
                logging.info("Using list number: " + str(count))
                logging.info(str(agree) + " is equal to " +str(road))
                agreement += 1

            else:
                logging.critical("Trouble in paradise")
                logging.critical(str(count))
            count += 1
        total += 1
    logging.info(str(agreement)+ " out of "+ str(total)+ " reached")
    logging.info("FINISHED - Nearest highway comparisons")

def make_deque(geocode_json, pair_id, count):
    """ Make deque if list contains data """
    if len(geocode_json[pair_id][0][count]) > 0:
        return deque(geocode_json[pair_id][0][count])
    else:
        logging.exception("List of length 0 returned, " +\
                          str(pair_id) + " for " + str(count))
        return None

def check_deque(near_highway, agree):
    """ Check deque for first str """
    if near_highway != None:
        while len(near_highway) > 0:
            peek = near_highway.popleft()
            
            if type(peek) == str or type(peek) == unicode:
                agree.append(peek)
                break
    if len(near_highway) == 0:
        logging.exception("All possibilities exhausted")
    # After checks, bring the queue back            
    return agree

def note_matches(agree):
    """ Change list to a set and review contents """
    check = set(agree)

    if len(check) > 1:
        while len(check) > 0:
            logging.critical("Not matching: "+ str(check.pop()))
        return False
        
    elif len(check) == 1:
        logging.info("Match found: "+str(check))
        return True
    else:
        logging.error("Something wrong with the set")
            
def nearest_road(geocode_json):
    """ Nearest road that's not None

    This approach is only returning an 'agreed upon' location for 74
    out of 155 pair_id's. Improvement by 12 but only finding  47% so
    that's a 7% improvement.

    Args:
        geocode_json: Geocode api written to json; can be accessed
                      using read_json()
    Returns:
        Just logs for now
    """
    logging.info("STARTED - Nearest highway comparisons")
    # Used for matches/total
    total = 0
    agreement = 0
    
    for pair_id in geocode_json.keys():

        # Used for matching
        count = 0
        agree = []
        logging.info("Using pair_id: "+ str(pair_id))
        while count < len(geocode_json[pair_id][0]):
            near_highway = make_deque(geocode_json, pair_id, count)

            if check_deque(near_highway, agree) != None:
                pass

            count += 1

        if note_matches(agree) == True:
            agreement += 1
        logging.info("Concluded processing for pair_id: "+str(pair_id))
        total += 1
    logging.info(str(agreement)+ " out of " + str(total)+ " found")
    logging.info("FINISHED - Nearest highway comparisons")

def make_set(geocode_json, pair_id, count):
    """ Make deque if list contains data """
    if len(geocode_json[pair_id][0][count]) > 0:
        return set(geocode_json[pair_id][0][count])
    else:
        logging.exception("List of length 0 returned, " +\
                          str(pair_id) + " for " + str(count))
        return None

def set_matches(agree):
    """ Compare sets to find intersection """
    first = True
    results = []
    if len(agree) < 2:
        return None
    while len(agree) > 0:
        if first:
            base = agree.pop()
            first = False
        else:
            for item in base - agree.pop():
                results.append(item)
    return set(results)

def finding_roads(geocode_json):
    """ Set intersections between coordinate pairs

    Alright, this approach returns 45 out of 155 coordinate pairs
    as matches. We decreased our accuracy to 29% with this method.
    It's about an 18% decline from nearest_road(). However, we were
    also about to extract partial matches.

    If we start to work with partial matches, about 64% were returned.
    This means that more than one highway name matched between sets.
    Since 'matches' and 'partially matches' are mutually exclusive,
    let's pretend that we can add these percentages together. That
    would put us at 93% if we were able to narrow down the multiple
    matches to one.

    However, it doesn't mean that the match that we found was
    meaningful. At this point it's probably best to drop the reverse
    geocoding API approach and start getting out the regex.

    Args:
        geocode_json: Geocode api written to json; can be accessed
                      using read_json()
    Returns:
        Just logs for now
    """
    logging.info("STARTED - Nearest highway comparisons")
    # Used for matches/total
    total = 0
    agreement = 0
    partial_matches = 0
    
    for pair_id in geocode_json.keys():

        # Used for matching
        count = 0
        agree = []
        logging.info("Using pair_id: "+ str(pair_id))
        while count < len(geocode_json[pair_id][0]):
            near_highway = make_set(geocode_json, pair_id, count)

            agree.append(near_highway)
            count += 1
        # alright, let's check out set intersections
        matches = set_matches(agree)
        if len(matches) > 1:
            logging.warning("Multiple matches found: "+str(matches))
            partial_matches += 1
        elif len(matches) == 1:
            logging.info("Match found: "+str(matches))
            agreement += 1
        elif len(matches) == 0:
            logging.error("No matches found: "+str(matches))
            
        else:
            logging.critical("Something else went wrong")
        total += 1
    logging.info(str(agreement)+" matches out of "+str(total)+" found")
    logging.info(str(partial_matches)+" partial matches out of "+\
                 str(total)+" found")
    logging.info("COMPLETED - Nearest highway comparisons")
        
def write_csv_file(datasource):
    """ Output, (pair_id, Route)
    """
    pass

def main():
    finding_roads(read_json())

if __name__ == "__main__":
    enable_log("highwayFinder")
    main()
