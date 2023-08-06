def remove_none_values(dictionary):
    filtered_dictionary = {key: value for key, value in dictionary.items()
                           if value is not None}
    return filtered_dictionary
