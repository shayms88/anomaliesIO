# Lists
def generate_unique_list_values(_list):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in _list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
            # print list
    return unique_list


# Dicts
def change_dict_keys_to_str_type(_dict):
    new_dict = {}
    for k,v in _dict.items():
        new_dict[str(k)] = v
    return new_dict


# Dataframes
def generate_subset_df_from_fields_list(df, fields_list):
    return df[fields_list]