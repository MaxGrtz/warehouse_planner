

def read_problem(path):
    '''
    helper method to read problem file 
        parameter: path - path of problem.txt file
        returns: item encoding dict, item decoding dict, dict of PSUs and their items
    '''

    try: 
        if "problem" not in path:
            raise NameError('name of file chosen does not contain "problem"')  # raise error if the name does not contain "problem"
        # open file
        with open(path, "r") as file:
            lines = file.readlines()

        # create encoding and decoding dictionaries
        items = lines.pop(0).split(' ')[:-1]  # pop the inventory list line and safe in items
        encode_dict = {}
        decode_dict = {}

        for c, item in enumerate(items):
            encode_dict[item] = c
            decode_dict[c] = item

        # create dict of PSUs with list of items they hold
        lines.pop(0) # pop the empty line, between inventory and PSUs
        psu_dict = {}
        for c,l in enumerate(lines):
            # psu_dict: key - PSU id (row number), value - list of numerically encoded items in the row 
            psu_dict[c] = [encode_dict[item] for item in l.split(' ') if not item in '\n'] 
    except:
        return None, None, None # return None for encoding, decoding and psu dict if there is some problem with the chosen file

    return encode_dict, decode_dict, psu_dict


def read_order(path, encode_dict):
    '''
    helper method to read order file
    parameters: path - path of order.txt file
                encode_dict - dict to encode items
    returns: list of encoded order items and missing item (items not in the inventory)
    '''
    try:
        if "order" not in path:
            raise NameError('name of file chosen does not contain "order"')  # raise error if the selected path does not contain "order"
        # read order file
        with open(path, "r") as file:
            order = file.readlines()[0].split(' ')
    except:
        return None, None  # return None for order and missing items lists if there is any problem when reading the file

    missing_items = []
    # encode items in order list, append item which are not in the dictionary (ie. not in the inventory)
    order = [encode_dict[item] if item in encode_dict else missing_items.append(item) for item in order]
    order = [item for item in order if item is not None] # filter out None values from order list

    return order, missing_items
