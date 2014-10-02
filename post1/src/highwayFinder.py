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

def parse_name(colname, pattern):
    """ Parse this based on the pattern """
    highway = re.compile("(\w-\d{2})|(^\d{2})|(^\d{3})|(^\w{3}\W{2}\d)")
    if highway.search(colname):
        return highway.search(colname).group(0) #first group assumption

    if pattern == 1:
        pattern = re.compile("")
        if pattern.search(colname) == None: 
    elif pattern == 2:
        pass
    elif pattern == 3:
        pass
    else:
        logging.critical("Incorrect pattern assigned: ", str(pattern))
        return False

def parse_description(colname):
    """ Parse out highway name from description
    
    Pulling highway names from the description given by the DOT. We're
    going to make a set of mutually exclusive rules about the contents
    of the description fields. We'll translate those rules to regular
    expressions.

    Args:
        datasource: dict, datastructure from read_description()
    Returns:
        dict, tuple, turns value of dict to a tuple containing the
        original string and the predicted highway location 
    """
    pattern = 0
    member = set(['before','after','to'])
    colset = set(colname.lower().split(" "))
    # If a value includes both 'before' and 'after' but also includes
    # 'TO' then identify the road before 'TO'
    if member <= colset: # is subset?
        pattern = 1
        parse_name(colname, pattern)
        
    # All highway names will be referenced ahead of the words 'before'
    # or 'after', unless those words are not used at all. 
    detach = member.pop()
    elif member in colset:
        pattern = 2
        parse_name(colname, pattern)

    # If 'before' or 'after' are not used then 'to' will be used.
    # The highway will be referenced before 'to'
    elif detach in colset:
        pattern = 3
        parse_name(colname, pattern)

    # We can't find a pattern for the description if we've reached
    # this point.
    else:
        logging.error("Pattern not matched: ", colname)
        return False

# run parse_description() through a for loop here        
def decide_nearest_highway(datasource):
    """ Decide which highway is closest to each pair_id """
    data = request_nearest_road(datasource)
    count = 0
    for pair_id in data.keys():
        start = data[pair_id].pop()
        if start != data[pair_id].pop():
            raise UserWarning("Something is amiss")
        else:
            print pair_id, "\t", count
            count += 1

def write_csv_file(datasource):
    """ Output, (pair_id, Route)
    """
    pass

def main():
    pass

if __name__ == "__main__":
    enable_log("highwayFinder")
    main()
