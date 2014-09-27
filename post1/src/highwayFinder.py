
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
