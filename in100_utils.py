import streamlit as st
import json
import pandas as pd
version_all = ["PHOENIX", "XX", "OLD"]
songtype_all = ["Arcade", "Remix", "Full Song", "Short Cut"]

current_date = "2024.05.16"
current_version = "PHOENIX"
current_patch = "1.0.8"

user_ranks = json.load(open(f"datamodules/in100RankData/{current_date}/user_data.json"))

total_steps_count = json.load(open(f"datamodules/{current_version}/{current_patch}/total_steps_count.json"))

duplicate_users = json.load(open("duplicate_users.json"))

#level_weight = {20: 8, 21: 10, 22: 14, 23: 22, 24: 38, 25: 70, 26: 134, 27: 262, 28: 518}
level_weight = {20: 8, 21: 10, 22: 14, 23: 20, 24: 28, 25: 38, 26: 50, 27: 64, 28: 70}
rank_weight = lambda x: (200-x)/200

def DA_0():
    return [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
def DA_l():
    return [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]

def songtype_to_int(songtype):
    if songtype == "Arcade":
        return 0
    elif songtype == "Remix":
        return 1
    elif songtype == "Full Song":
        return 2
    elif songtype == "Short Cut":
        return 3
    else:
        return -1

def version_to_int(version):
    if version == "PHOENIX":
        return 0
    elif version == "XX":
        return 1
    else:
        return 2

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

def add_dict(a, b):
    for item in b:
        if item in a:
            a[item] += b[item]
        else:
            a[item] = b[item]
    return a

def get_song_version_int_list(songtype, version):
    songtypeint = []
    for item in songtype:
        songtypeint.append(songtype_to_int(item))
    versionint = []
    for item in version:
        versionint.append(version_to_int(item))
    return songtypeint, versionint

def filter_total_count_unit(total_count, mode, levels =[20,28], songtype = songtype_all, version = version_all):
    levels = restrict_level_range(mode, levels)
    if levels[0] == -1:
        print("Error in level range")
        return {}
    count = {key: 0 for key in range(levels[0], levels[1]+1)}
    #print(count)
    songtypeint, versionint = get_song_version_int_list(songtype, version)
    #print(data["single_counts"])
    for level in range(levels[0], levels[1]+1):
        str_level = str(level)
        for songtype in songtypeint:
            for version in versionint:
                if mode == "Single":
                    #print(count[level])
                    #print(data["single_counts"][str_level][songtype][version])
                    count[level] += total_count["Single"][str_level][songtype][version]
                else:
                    count[level] += total_count["Double"][str_level][songtype][version]
    return count

def filter_total_count(total_count, mode = "Full", levels =[20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_total_count_unit(total_count, "Single", levels, songtype, version)
        dictb = filter_total_count_unit(total_count, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_total_count_unit(total_count, mode, levels, songtype, version)

def filter_rankdata_unit(data, mode, levels =[20,28], songtype = songtype_all, version = version_all):

    levels = restrict_level_range(mode, levels)
    if levels[0] == -1:
        print("Error in level range")
        return {}
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

def filter_rankdata(data, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_rankdata_unit(data, "Single", levels, songtype, version)
        dictb = filter_rankdata_unit(data, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_rankdata_unit(data, mode, levels, songtype, version)

def filter_rankcount_unit(data, mode, levels = [20,28], songtype = songtype_all, version = version_all):
    levels = restrict_level_range(mode, levels)

    if levels[0] == -1:
        print("Error in level range")
        return {}
    count = {key: 0 for key in range(levels[0], levels[1]+1)}
    #print(count)
    songtypeint, versionint = get_song_version_int_list(songtype, version)
    #print(data["single_counts"])
    for level in range(levels[0], levels[1]+1):
        str_level = str(level)
        for songtype in songtypeint:
            for version in versionint:
                if mode == "Single":
                    #print(count[level])
                    #print(data["single_counts"][str_level][songtype][version])
                    count[level] += data["single_counts"][str_level][songtype][version]
                else:
                    count[level] += data["double_counts"][str_level][songtype][version]
    return count

def filter_rankcount(data, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_rankcount_unit(data, "Single", levels, songtype, version)
        dictb = filter_rankcount_unit(data, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_rankcount_unit(data, mode, levels, songtype, version)


def rankdata_unit_str(data):
    mode = "D"
    if data["mode"] == "Single": mode = "S"

    return data["song"] + " " + mode + str(data["level"]) + ": rank " + str(data["rank"]) + ", score: " + str(data["score"])
    
def total_count(data):
    total = 0
    for level in data:
        total += data[level]
    return total

def total_count_weighted(data):
    total = 0
    for level in data:
        total += data[level]*level_weight[level]
    return total

def total_count_with_rank(data):
    total = 0
    for level in data:
        for ranks in range(len(data[level])):
            total += level*rank_weight(data[level][ranks]["rank"])
    return total

def total_count_with_rank_weighted(data):
    total = 0
    for level in data:
        for ranks in range(len(data[level])):
            total += level*rank_weight(data[level][ranks]["rank"])*level_weight[level]
    return total

def sort_rankdata(data, sort_key = "score", sort_all = False):
    if sort_all == False:
        for level in data:
            if sort_key == "score":
                data[level].sort(key = lambda x: x['score'], reverse = True)
            elif sort_key == "rank":
                data[level].sort(key = lambda x: x['rank'])
        total_list = []
        for level in sorted(data.keys(), reverse= True):
            total_list += data[level]
    else:
        total_list = []
        for level in sorted(data.keys(), reverse= True):
            total_list += data[level]
        if sort_key == "score":
            total_list.sort(key = lambda x: x['score'], reverse = True)
        elif sort_key == "rank":
            total_list.sort(key = lambda x: x['rank'])
    return total_list

def search_user(username, exact = False):
    usernames = {}   
    search_term = username.upper()

    # Iterate through each user in the user ranks list
    for user in user_ranks:
        # Check if the search term is in the current username in the list
        if search_term in user["username"].upper():
            cleardata = filter_rankcount(user)
            # Add or append the userID to the usernames dictionary
            if exact == False:
                if user["username"] not in usernames:
                    usernames[user["username"]] = [[user["userID"], cleardata]]
                else:
                    usernames[user["username"]].append([user["userID"], cleardata])
            else:
                if user["username"] == search_term:
                    if user["username"] not in usernames:
                        usernames[user["username"]] = [[user["userID"], cleardata]]
                    else:
                        usernames[user["username"]].append([user["userID"], cleardata])
            
    return usernames

def print_search_user(username, exact = False):
    strs = []
    printme = search_user(username, exact)
    for user in printme:
        strs.append(user)
        for item in printme[user]:
            strs.append(item[0]+": "+str(item[1]))
        strs.append("")
    return strs

def return_user(username, userID):
    if len(userID) == 4:
        userID = "#" + str(userID)
    for user in user_ranks:
        if user["username"] == username and user["userID"] == userID:
            return user 
    return None

def return_user_with_name(username):
    username_upper = username.upper()
    if username_upper in duplicate_users:
        str1 = "Duplicate users found"
        str2 = "Please search with the following format: [username] [userID]"
        str3 = "The First User is selected among: \n"
        str4 = print_search_user(username_upper, exact = True)
        print(str1)
        print(str2)
        print(str3)
        for item in str4:
            print(item)
        strs = [str1, str2, str3, str4]
        userID = search_user(username_upper, exact = True)[username_upper][0][0]
        return return_user(username_upper, userID)
    if " " in username:
        username, userID = username.split(" ")
        username_upper = username.upper()
    else:
        userID = search_user(username_upper, exact = True)[username_upper][0][0]
    return return_user(username_upper, userID)

def rankdata_raw(username, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    user = return_user_with_name(username)
    
    userCount = filter_rankcount(user, mode, levels, songtype, version)
    userData = filter_rankdata(user, mode, levels, songtype, version)
    total_filtered = filter_total_count(total_steps_count, mode, levels, songtype, version)
    return userData, userCount, total_filtered
    #

def rankdata_compare_raw(userAname, userBname, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    userA = return_user_with_name(userAname)
    userB = return_user_with_name(userBname)
    userAcount = filter_rankcount(userA, mode, levels, songtype, version)
    userBcount = filter_rankcount(userB, mode, levels, songtype, version)
    userAdata = filter_rankdata(userA, mode, levels, songtype, version)
    userBdata = filter_rankdata(userB, mode, levels, songtype, version)
    total_filtered = filter_total_count(total_steps_count, mode, levels, songtype, version)
    return userAdata, userBdata, userAcount, userBcount, total_filtered

def color_rows(row, userAkey):
    # Use RGBA for semi-transparent colors (the last number is the alpha value)
    # The alpha value can be adjusted between 0 (fully transparent) and 1 (fully opaque)
    # Here we set it to 0.5 to blend the color with the white background, making it lighter
    color = 'rgba(125, 50, 50, 0.5)' if row['Winner'] != userAkey else 'rgba(50,50,125, 0.5)'
    return ['background-color: ' + color] * len(row)

def aggregate_dataframe(userA_data, userB_data, userA, userB):
    aggregated_dict = sort_rankdata(add_dict(userA_data, userB_data), "score", False)
    userAkey = userA["key"]
    userBkey = userB["key"]
    Arank = userA["username"] + "_rank"
    Brank = userB["username"] + "_rank"
    Ascore = userA["username"] + "_score"
    Bscore = userB["username"] + "_score"
    pd_aggregated = pd.DataFrame(columns = ["song", "mode", "level", userAkey, Arank, Ascore, userBkey, Brank, Bscore])
    
    pd_list = []
    pd_keys = []
    for item in aggregated_dict:
        #print(item)
        mode = "D"
        if item["mode"] == "Single": mode = "S"
        key = item["song"] + " " + mode + str(item["level"])
        if key not in pd_keys:
            pd_list.append(create_dict(item, userA, userB))
            pd_keys.append(key)
        else:
            for occupied in pd_list:
                #print(item)
                if occupied["key"] == key:
                    if occupied[Ascore] == 0:
                        occupied[Arank] = item["rank"]
                        occupied[Ascore] = item["score"]
                    else:
                        occupied[Brank] = item["rank"]
                        occupied[Bscore] = item["score"]
    pd_aggregated = pd.DataFrame(pd_list)


    winner = []
    for item in pd_list:
        if item[Ascore] > item[Bscore]:
            winner.append(userAkey)
        elif item[Ascore] < item[Bscore]:
            winner.append(userBkey)
        else:
            winner.append("DRAW")
    pd_aggregated["Winner"] = winner
    pd_aggregated = pd_aggregated.drop("key", axis = 1)
    
    pd_aggregated = pd_aggregated.style.apply(color_rows, userAkey = userAkey, axis = 1)
    
    return pd_aggregated

def create_dict(item, userA, userB):
    userAkey = userA["key"]
    userBkey = userB["key"]
    Arank = userA["username"] + "_rank"
    Brank = userB["username"] + "_rank"
    Ascore = userA["username"] + "_score"
    Bscore = userB["username"] + "_score"
    mode = "D"
    if item["mode"] == "Single": mode = "S"
    level_short = mode + str(item["level"])
    key = item["song"] + " " + level_short
    if item["username"] == userAkey[:-6]:
        return {"key":key, "song": item["song"], "level": level_short, Arank: item["rank"], Ascore: item["score"], Brank: "-", Bscore: 0}
    else:
        return {"key":key, "song": item["song"], "level": level_short, Arank: "-", Ascore: 0, Brank: item["rank"], Bscore: item["score"]}

def refine_solo_dataframe(dataframe_raw):
    levelmode = []
    #print(dataframe_raw)
    for index, row in dataframe_raw.iterrows():
        mode_short = "D"
        if row["mode"] == "Single": mode_short = "S"
        levelmode.append(mode_short+str(row["level"]))


    dataframe_raw["mode/level"] = levelmode

    dataframe_new = dataframe_raw[["song", "mode/level", "rank", "score"]]
    return dataframe_new

#data_sorted_pandas, achievement_rate, ranks, ranks_by_level
def rankdata(username, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all, sortme = "score", sort_all = False):
    data_user,count_user,total_user = rankdata_raw(username, mode, levels, songtype, version)
    data_sorted = sort_rankdata(data_user, sortme, sort_all)
    if len(data_sorted) != 0:
        data_sorted_pandas_raw = pd.DataFrame(data_sorted)
        data_sorted_pandas = refine_solo_dataframe(data_sorted_pandas_raw)
    else:
        data_sorted_pandas = pd.DataFrame()
    achievement_rate = {}
    for item in count_user:
        if total_user[item] == 0: 
            achievement_rate[item] = 0
        else:
            achievement_rate[item] = round(count_user[item]/total_user[item],3)
    ranks = []
    for item in data_sorted:
        ranks.append(item["rank"])
    ranks.sort()
    ranks_by_level = {}
    for item in data_sorted:
        if item["level"] not in ranks_by_level:
            ranks_by_level[item["level"]] = [item["rank"]]
        else:
            ranks_by_level[item["level"]].append(item["rank"])
    for item in ranks_by_level:
        ranks_by_level[item].sort()
    return data_sorted_pandas, count_user, achievement_rate, ranks, ranks_by_level

def rankdata_compare_total_counts(userAcount, userBcount, userAdata, userBdata):
    userA_total_count = total_count(userAcount)
    userB_total_count = total_count(userBcount)
    userA_total_count_weighted = total_count_weighted(userAcount)
    userB_total_count_weighted = total_count_weighted(userBcount)
    userA_total_count_with_rank = total_count_with_rank(userAdata)
    userB_total_count_with_rank = total_count_with_rank(userBdata)
    userA_total_count_with_rank_weighted = total_count_with_rank_weighted(userAdata)
    userB_total_count_with_rank_weighted = total_count_with_rank_weighted(userBdata)
    return [[userA_total_count, userB_total_count],
            [userA_total_count_weighted, userB_total_count_weighted], 
            [userA_total_count_with_rank, userB_total_count_with_rank], 
            [userA_total_count_with_rank_weighted, userB_total_count_with_rank_weighted]]


#user_comparison:
#0: userA_data_sorted, userB_data_sorted
#1: userA_achievement_rate, userB_achievement_rate
#2: userA_ranks, userB_ranks
#3: userA_ranks_by_level, userB_ranks_by_level
#total_count_comparison:
#0: userA_total_count, userB_total_count
#1: userA_total_count_weighted, userB_total_count_weighted
#2: userA_total_count_with_rank, userB_total_count_with_rank
#3: userA_total_count_with_rank_weighted, userB_total_count_with_rank_weighted
#aggregated_dataframe for comparison
def rankdata_compare(userA, userB,mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    userA_raw = return_user_with_name(userA)
    userB_raw = return_user_with_name(userB)
    userAdata, userBdata, userAcount, userBcount, total_filtered = rankdata_compare_raw(userA, userB, mode, levels, songtype, version)
    userA_data_sorted, userA_counts, userA_achievement_rate, userA_ranks, userA_ranks_by_level = rankdata(userA, mode, levels, songtype, version)
    userB_data_sorted, userB_counts, userB_achievement_rate, userB_ranks, userB_ranks_by_level = rankdata(userB, mode, levels, songtype, version)
    user_comparison = [[userA_data_sorted, userB_data_sorted], [userA_achievement_rate, userB_achievement_rate], [userA_ranks, userB_ranks], [userA_ranks_by_level, userB_ranks_by_level]]
    total_count_comparison = rankdata_compare_total_counts(userAcount, userBcount, userAdata, userBdata)
    aggregated_dataframe = aggregate_dataframe(userAdata, userBdata, userA_raw, userB_raw)
    return user_comparison, total_count_comparison, aggregated_dataframe

#