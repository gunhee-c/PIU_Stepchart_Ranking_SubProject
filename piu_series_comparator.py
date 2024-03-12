from enum import Enum

def get_series_rank(series):
        if series == "The 1st Dance Floor":
            return 1
        if series == "2nd Ultimate Remix":
            return 2
        if series == "3rd O.B.G":
            return 3
        if series == "The O.B.G / Season Evolution":
            return 4
        if series == "The Collection":
            return 5
        if series == "The Perfect Collection":
            return 6
        if series == "Extra":
            return 7
        if series == "The Premiere":
            return 8
        if series == "The Prex":
            return 9
        if series == "The Rebirth":
            return 10
        if series == "The Premiere 2":
            return 11
        if series == "The Prex 2":
            return 12
        if series == "The Premiere 3":
            return 13
        if series == "The Prex 3":
            return 14
        if series == "Exceed":
            return 15
        if series == "Exceed 2":
            return 16
        if series == "Zero":
            return 17
        if series == "NX / New Xenesis":
            return 18
        if series == "Pro":
            return 19
        if series == "NX2 / Next Xenesis":
            return 20
        if series == "NX Absolute":
            return 21
        if series == "Fiesta":
            return 22
        if series == "Pro2":
            return 23
        if series == "Fiesta EX":
            return 24
        if series == "Fiesta 2":
            return 25
        if series == "Infinity":
            return 26
        if series == "Prime":
            return 27
        if series == "Prime JE":
            return 28
        if series == "Prime 2":
            return 29
        if series == "XX":
            return 30
        if series == "Phoenix":
            return 31
        print("Error: Series not found")
        return -1

def get_version_detail_rank(series):
        if series == "default":
            return -1
        else:
            parts = series[1:].split('.')
            new_version = '.'.join(parts[:2]) + ''.join(parts[2:])
            try:
                return float(new_version)
            except:
                print("Error: Version not found")
                return 6974

def get_rank_float(series, version):
    series_rank = get_series_rank(series) * 100
    version_rank = get_version_detail_rank(version)
    return series_rank + version_rank 

def find_earliest_version(series_list, version_list):
    selectme = 0
    for i in range(len(version_list)):
        if get_rank_float(series_list[i], version_list[i]) <= get_rank_float(series_list[selectme], version_list[selectme]):
            selectme = i
    return series_list[selectme], version_list[selectme]
