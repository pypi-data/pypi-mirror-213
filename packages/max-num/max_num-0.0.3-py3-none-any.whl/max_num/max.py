class Max:
    def max_num_dict(dict):
        max_val = 0
        max_key = ""
        for (key_name,val) in dict.items():
            if max_val < val:
                max_val = val
                max_key = key_name
            else:
                max_val = max_val
                max_key = max_key
        result = {
            f"{max_key}":max_val
        }
        return result
    def max_num_list(List):
        max_val = 0
        for num in List:
            if max_val < num:
                max_val = num
            else:
                max_val = max_val
        return max_val
    def max_num(*args):
        max_val = 0
        for num in args:
            if max_val < num:
                max_val = num
            else:
                max_val = max_val
        return max_val
    