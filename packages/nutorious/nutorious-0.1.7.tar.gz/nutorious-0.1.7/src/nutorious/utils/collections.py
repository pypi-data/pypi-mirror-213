def merge_dicts(dict1, dict2, *other_dicts):
    result = dict1.copy()

    for d in [dict2, *other_dicts]:
        for k, v in d.items():
            if k in result and type(result[k]) == dict and type(v) == dict:
                result[k] = merge_dicts(result[k], v)
            else:
                result[k] = v

    return result
