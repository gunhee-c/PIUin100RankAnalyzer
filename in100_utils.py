import streamlit as st
import json
import pandas as pd
from in100_utils_variable import *
from in100_utils_submodules import *



def filter_total_count(total_count, mode = "Full", levels =[20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_total_count_unit(total_count, "Single", levels, songtype, version)
        dictb = filter_total_count_unit(total_count, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_total_count_unit(total_count, mode, levels, songtype, version)

def filter_rankdata(data, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_rankdata_unit(data, "Single", levels, songtype, version)
        dictb = filter_rankdata_unit(data, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_rankdata_unit(data, mode, levels, songtype, version)

def filter_rankcount(data, mode = "Full", levels = [20,28], songtype = songtype_all, version = version_all):
    if mode == "Full":
        dicta = filter_rankcount_unit(data, "Single", levels, songtype, version)
        dictb = filter_rankcount_unit(data, "Double", levels, songtype, version)
        return add_dict(dicta, dictb)
    else:
        return filter_rankcount_unit(data, mode, levels, songtype, version)

def rankdata_to_str(data):
    mode = "S" if data["mode"] == "Single" else "D"


    return data["song"] + " " + mode + str(data["level"]) + ": rank " + str(data["rank"]) + ", score: " + str(data["score"])

#apply this on filtered count
def total_count(data, level_weight = False, rank_weight = False):
    if level_weight == False and rank_weight == False:
        return total_count_raw(data)
    elif level_weight == True and rank_weight == False:
        return total_count_level_weighted(data)
    elif level_weight == False and rank_weight == True:
        return total_count_rank_weighted(data)
    else:
        return total_count_full_weighted(data)


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

#해당 str을 포함하는 유저들의 ID 리스트와 클리어데이터(숫자만)를 반환
def search_user(username, exact = False):
    usernames = {}   
    search_term = username.upper()

    # Iterate through each user in the user ranks list
    for user in user_names_dict:
        # Check if the search term is in the current username in the list
        if search_term in user:
            user_id_list = user_names_dict[user]
            cleardata = []
            for user_id in user_id_list:
                user_cleardata = filter_rankcount(return_user(user, user_id))
                cleardata.append(user_cleardata)
            user_cleardata_dict = dict(zip(user_id_list, cleardata))
            # Add or append the userID to the usernames dictionary
            if exact == False:
                usernames[user] = user_cleardata_dict
            elif user == search_term:
                usernames[user] = user_cleardata_dict
    return usernames

def print_search_user(username, exact = False):
    strs = []
    printme = search_user(username, exact)
    for user in printme:
        strs.append(user)
        for item in printme[user]:
            strs.append(item +" // cleardata: " +str(printme[user][item]))
        strs.append("")
    return strs




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
        mode = "S" if item["mode"] == "Single" else "D"
        key = item["song"] + " " + mode + str(item["level"])
        if key not in pd_keys:
            pd_list.append(create_dict(item, userA, userB))
            pd_keys.append(key)
        else:
            for occupied in pd_list:
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
    
    pd_aggregated = pd_aggregated.style.apply(color_rows_comparison, userAkey = userAkey, axis = 1)
    
    return pd_aggregated

def create_dict(item, userA, userB):
    userAkey = userA["key"]
    userBkey = userB["key"]
    Arank = userA["username"] + "_rank"
    Brank = userB["username"] + "_rank"
    Ascore = userA["username"] + "_score"
    Bscore = userB["username"] + "_score"
    mode = "S" if item["mode"] == "Single" else "D"
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

def color_by_level_and_rank(dataframe_raw):
    dataframe_new = dataframe_raw.copy()
    dataframe_new = dataframe_new.style.applymap(lambda x: 'color: red' if x == 1 else 'color: blue' if x == 2 else 'color: green' if x == 3 else 'color: black')
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