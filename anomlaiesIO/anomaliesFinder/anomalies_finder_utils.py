import csv

def parse_io_string_to_list_of_lists(io_string):
    final_list = []
    for row in csv.reader(io_string, delimiter=','):
        final_list.append(row)

    return {'columns_names':final_list[0],
            'data':final_list[1:]}