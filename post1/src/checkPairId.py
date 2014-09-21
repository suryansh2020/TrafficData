""" Account for PairID across data sources.

Given pair_id, match 'massdot_bluetoad_data$pair_id' with
'pair_definitions$pair_id' to make sure no ids are unaccounted.
Next, group 'massdot_bluetoad_data$pair_id' and see if we can account
for pair_routes.xml; <PairID>. If we are unable to account for all
pair Ids then figure it out. Hopefully, it's fine.
"""

massdot_bluetoad_data = False
pair_definitions = False
pair_routes = False

def parse_xml(datasource):
    """ Parse XML for pairId """
    pass

def parse_csv(datasource):
    """ Parse CSV file for pairId """
    pass

def check_ids(pairIds,*args):
    """ Check ids to see if any are missing

    Args:
        pairIds: str, list of pairIds
        *args: str, list of pairIds for however many datasources
    Returns:
        Boolean: True if all IDs are present in all datasources
    """
    base = set(pairIds)
    for list_of_ids in *args:
        # Check for differences between lists by using sets.
        if len(set(list_of_ids) - base) != 0:
            raise TypeError(str(list_of_ids), " missing value")
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
