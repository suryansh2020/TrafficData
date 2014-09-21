""" Account for PairID across data sources.

Given pair_id, match 'massdot_bluetoad_data$pair_id' with
'pair_definitions$pair_id' to make sure no ids are unaccounted.
Next, group 'massdot_bluetoad_data$pair_id' and see if we can account
for pair_routes.xml; <PairID>. If we are unable to account for all
pair Ids then figure it out. Hopefully, it's fine.
"""
import csv
import os
import sys
from collections import Counter

def datasources():
    """ Location for the datasources

    This approach seemed easier than passing the datasources on the
    command line since we already know which data we'll be using.

    Returns:
        Tuple of strings, each string is a filepath to the datasources
        we need. (massdot_bluetoad_data,pair_definitions,pair_routes)
    """
    folder_location = os.path.abspath("")+ \
                      "/MassDOThack/Road_RTTM_Volume/"
    # check that script was called at the correct place in the
    # directory 
    cnt = Counter(folder_location.split("/"))
    if cnt["MassDOThack"] > 1 or cnt["Road_RTTM_Volume"] > 1:
        raise UserWarning("Please run this file at ~/TrafficData")

    # now we can create file paths to our datasources
    massdot_bluetoad_data = folder_location + \
                                "massdot_bluetoad_data/" + \
                                "massdot_bluetoad_data.csv"
    pair_definitions = folder_location + \
                           "pair_definitions.csv"
    pair_routes = folder_location + \
                  "pair_routes.xml"
    # return the paths in order specified in docstring
    return (massdot_bluetoad_data, pair_definitions, pair_routes)

def parse_xml(datasource):
    """ Parse XML for pairId """
    pass

def use_correct_csv_column(datasource):
    """ Let's make sure we're grabbing pair_id
    Returns:
        A number where the index matches the pair_id column
    """
    return datasource.index("pair_id")
    

def parse_csv(datasource):
    """ Parse CSV file for pairId """
    pair_ids = []
    with open(datasource, 'rb') as f:
        header = True
        reader = csv.reader(f, delimiter = ",", quotechar = "")
        # attempt to return a list of strings, where each string
        # is a pairID
        try:
            for row in reader:
                if header == True:
                    index_me = use_correct_csv_column(row)
                    header = False
                else:
                    pair_ids.append(row[index_me])
            return pair_ids
        # if there's something wrong with the csv file then raise an
        # error.
        except csv.Error as e:
            sys.exit('datasource %s, line %d: %s' % (datasource,
                                                     reader.line_num,
                                                     e))
                                
def check_input_type(data):
    """ Data: str, list of pairIds """
    if type(data[0]) != str:
        raise TypeError(str(data), " contains wrong type")
    else:
        return True

def check_ids(pairIds,*args):
    """ Check ids to see if any are missing

    Args:
        pairIds: str, list of pairIds
        *args: str, list of pairIds for however many datasources
    Returns:
        Boolean: True if all IDs are present in all datasources
    """
    if check_input_type(pairIds) == True:
        base = set(pairIds)
    # compare other datasources
    for list_of_ids in args:
        # Check for differences between lists by using sets.
        if check_input_type(list_of_ids) == True and \
           len(set(list_of_ids) - base) != 0:
            raise UserWarning(str(list_of_ids), " missing value")
        else:
            pass
    return True

def main(*args):
    """ Parse datasources and check for consistent pairID """

    if check_ids(parse_csv(datasource1),
                 parse_csv(datasource2),
                 parse_xml(datasource3)) == True:
        print "Success -- Ids match across datasources"
    else:
        print "Failure -- TypeError should have been raised by now"
            

if __name__ == "__main__":
    main()
