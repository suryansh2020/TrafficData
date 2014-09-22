"""
Outputs a csv file (pair_id, route)

This includes the logic for deciding the correct road when using
reverse geocoding. 
"""

def datasources():
    """ Location for the datasources

    Instead of passing the filepaths on the command line we just call
    this function since we already know what we need.

    Returns:
        Tuple of strings, each string is a filepath to a datasource.
        (pair_routes)
    """
    pass

def parse_pair_id(datasource):
    """ Returns each pair ID
    """
    pass

def parse_routes(datasource):
    """ Returns each child of routes where pair ID is the parent
    """
    pass

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
    pass

if __name__ == "__main__":
    main()

