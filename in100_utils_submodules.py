from in100_utils_variable import *

def restrict_level_range(mode, levels):
    ans = [0,0]
    ans[0] = levels[0]
    ans[1] = levels[1]
    #print(levels)
    if mode == "Single":
        if levels[1] > 26: ans[1] = 26
    else:
        if levels[1] > 28: ans[1] = 28
    if levels[0] < 20:
        ans[0] = 20
    if levels[0] > levels[1]:
        return [-1,-1]
    return ans

#SongType과 Version을 받아서 이에 해당하는 int값을 반환: Enum에 해당하는 기능
def get_song_version_int_list(songtype, version):
    songtypeint = []
    for item in songtype:
        songtypeint.append(songtype_to_int(item))
    versionint = []
    for item in version:
        versionint.append(version_to_int(item))
    return songtypeint, versionint

def add_dict(a, b):
    for item in b:
        if item in a:
            a[item] += b[item]
        else:
            a[item] = b[item]
    return a

#필터링에 대응해 총 스텝 수를 조정하여 반환
def filter_total_count_unit(total_count, mode, levels =[20,28], songtype = songtype_all, version = version_all):
    levels = restrict_level_range(mode, levels)
    count = {key: 0 for key in range(levels[0], levels[1]+1)}
    songtypeint, versionint = get_song_version_int_list(songtype, version)
    for level in range(levels[0], levels[1]+1):
        str_level = str(level)
        for songtype in songtypeint:
            for version in versionint:
                if mode == "Single":
                    count[level] += total_count["Single"][str_level][songtype][version]
                else:
                    count[level] += total_count["Double"][str_level][songtype][version]
    return count

def filter_rankdata_unit(data, mode, levels =[20,28], songtype = songtype_all, version = version_all):

    levels = restrict_level_range(mode, levels)
    filtered_rank = {key: [] for key in range(levels[0], levels[1]+1)}

    songtypeint, versionint = get_song_version_int_list(songtype, version)
    #print(songtypeint, versionint)
    for level in range(levels[0], levels[1]+1):
        str_level = str(level)
        for songtype in songtypeint:
            for version in versionint:
                    if mode == "Single":
                        for item in data["single_data"][str_level][songtype][version]:
                            filtered_rank[level].append(item)
                    else:
                        for item in data["double_data"][str_level][songtype][version]:
                            filtered_rank[level].append(item) 
    return filtered_rank

def filter_rankcount_unit(data, mode, levels = [20,28], songtype = songtype_all, version = version_all):
    levels = restrict_level_range(mode, levels)
    count = {key: 0 for key in range(levels[0], levels[1]+1)}
    songtypeint, versionint = get_song_version_int_list(songtype, version)
    for level in range(levels[0], levels[1]+1):
        str_level = str(level)
        for songtype in songtypeint:
            for version in versionint:
                if mode == "Single":
                    count[level] += data["single_counts"][str_level][songtype][version]
                else:
                    count[level] += data["double_counts"][str_level][songtype][version]
    return count


def total_count_raw(data):
    total = 0
    for level in data:
        total += data[level]
    return total

def total_count_level_weighted(data):
    total = 0
    for level in data:
        total += data[level]*level_weight[level]
    return total

def total_count_rank_weighted(data):
    total = 0
    for level in data:
        for ranks in range(len(data[level])):
            total += level*rank_weight(data[level][ranks]["rank"])
    return total

def total_count_full_weighted(data):
    total = 0
    for level in data:
        for ranks in range(len(data[level])):
            total += level*rank_weight(data[level][ranks]["rank"])*level_weight[level]
    return total



def return_user_with_name(username):
    username_upper = username.upper()
    if " " in username:
        username, userID = username.split(" ")
        username_upper = username.upper()
    else:
        userID = return_user_id_list(username_upper)[0]
    return return_user(username_upper, userID)

def return_user(username, userID):
    if len(userID) == 4:
        userID = "#" + str(userID)
    username_full = username + " " + userID
    return user_ranks[username_full]


def return_user_id_list(username):
    return user_names_dict[username.upper()]

def color_rows_comparison(row, userAkey):
    # Use RGBA for semi-transparent colors (the last number is the alpha value)
    # The alpha value can be adjusted between 0 (fully transparent) and 1 (fully opaque)
    # Here we set it to 0.5 to blend the color with the white background, making it lighter
    if row["Winner"] == "DRAW":
        color = 'rgba(160, 160, 60, 0.5)'
    else:
        color = 'rgba(125, 50, 50, 0.5)' if row['Winner'] != userAkey else 'rgba(50,50,125, 0.5)'
    return ['background-color: ' + color] * len(row)