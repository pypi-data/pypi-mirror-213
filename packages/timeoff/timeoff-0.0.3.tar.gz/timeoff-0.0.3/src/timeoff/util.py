def print_ordinal(number):
    th_min_range = 10
    th_max_range = 20
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    suffix = "th" if th_min_range < number < th_max_range else suffixes.get(number % 10, "th")
    return f"{number}{suffix}"
