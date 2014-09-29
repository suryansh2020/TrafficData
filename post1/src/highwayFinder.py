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
"""
import os
import io
import json

def read_json():
    """ Reading in json data from geocode api 

    Bypassing tests that the user is in the correct directory because
    they should have figured it out by now.
    """
    da_path = os.path.abspath("")+ "/post1/src/geocode.txt"
    # needs to support utf-8
    with io.open(da_path, 'r', encoding="utf-8") as f:
        return json.load(f)
    





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
    main()
