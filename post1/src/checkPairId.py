""" Account for PairID across data sources.

Given pair_id, match 'massdot_bluetoad_data$pair_id' with
'pair_definitions$pair_id' to make sure no ids are unaccounted.
Next, group 'massdot_bluetoad_data$pair_id' and see if we can account
for pair_routes.xml; <PairID>. If we are unable to account for all
pair Ids then figure it out. Hopefully, it's fine.

There are differences between datasets. Lets log the differences &
go from there.
"""
import csv
import os
import sys
import logging
from collections import Counter
import xmltodict

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
    """ Parse XML for pairId
    
    If this function used xpath, I'd feel much better about it.
    http://docs.python-guide.org/en/latest/scenarios/xml/

    Args:
        datasource: str, path to xml file
    Returns:
        list of strings, each string is a PairID
    """
    ids_we_want = []
    with open(datasource) as fd:
        obj = xmltodict.parse(fd.read())
        # xml has been converted to a python dictionary,
        # iterating through the dictionary to get all of the ids
        for pair_id in \
            range(len(obj[u'btdata'][u'TRAVELDATA'][u'PAIRDATA'])):
            # get each PairID child
            get_this = obj[u'btdata'][u'TRAVELDATA']\
                       [u'PAIRDATA'][pair_id][u'PairID']
            ids_we_want.append(get_this)
        return ids_we_want

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
        reader = csv.reader(f, delimiter = ",")
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
def enable_log(log_name):
    """ Enable logs written to file """
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG)


def check_input_type(data):
    """ Data: str, list of pairIds """
    if type(data[0]) != str and type(data[0]) != unicode:
        raise TypeError(str(data), " contains wrong type")
    else:
        return True

def check_ids(pairIds,*args):
    """ Check ids to see if any are different

    Note that this will check to see if the IDs are different but
    they will not check to see if a list is incomplete.

    Args:
        pairIds: str, list of pairIds
        *args: str, list of pairIds for however many datasources
    Returns:
        Boolean: True if all IDs are present in all datasources
    """
    logging.info('Beginning to check pair_id across datasources')
    if check_input_type(pairIds) == True:
        base = set(pairIds)
        logging.info('Param 0 converted to a set')
    # compare other datasources
    param_count = 0
    for list_of_ids in args:
        param_count += 1
        logging.info('Param ' +str(param_count)+' converted to a set')
        # Check for differences between lists by using sets.
        if check_input_type(list_of_ids) != True:
            logging.debug("[E1] Input type not a string or unicode")
        if len(set(list_of_ids) - base) != 0:
            logging.warning("Param # members not present in Param 0")
            logging.debug("[E2] Difference " + \
                          str(set(list_of_ids) - base))
            raise UserWarning(str(list_of_ids), " missing value")
        if len(base - set(list_of_ids)) != 0:
            logging.warning("Param 0  members not present in Param #")
            logging.debug("[E2] Difference " + \
                          str(base - set(list_of_ids)))
        else:
            pass
    return True

def main(*args):
    """ Parse datasources and check for consistent pairID """
    # get data
    datasource1, datasource2, datasource3 = datasources()
    logging.info("param 0 is: " +str(datasource1))
    logging.info("param 1 is: " +str(datasource2))
    logging.info("param 2 is: " +str(datasource3))
    # see if there's problems with pair_id
    if check_ids(parse_csv(datasource1),
                 parse_csv(datasource2),
                 parse_xml(datasource3)) == True:
        print("Review logs for missing Ids")
    else:
        print("Failure -- TypeError should have been raised by now")
            

if __name__ == "__main__":
    enable_log("differences")
    main()
