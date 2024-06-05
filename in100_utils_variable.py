import json
import pandas as pd
version_all = ["PHOENIX", "XX", "OLD"]
songtype_all = ["Arcade", "Remix", "Full Song", "Short Cut"]

current_date = "2024.05.16"
current_version = "PHOENIX"
current_patch = "2.0.0"

#level_weight = {20: 8, 21: 10, 22: 14, 23: 22, 24: 38, 25: 70, 26: 134, 27: 262, 28: 518}
level_weight = {20: 8, 21: 10, 22: 14, 23: 20, 24: 28, 25: 38, 26: 50, 27: 64, 28: 70}
rank_weight = lambda x: (200-x)/200



user_ranks = json.load(open(f"datamodules/in100RankData/{current_date}/user_data.json"))

user_names_dict = json.load(open(f"datamodules/in100RankData/{current_date}/user_dict.json"))

total_steps_count = json.load(open(f"datamodules/{current_version}/{current_patch}/total_steps_count.json"))

songlist_csv = pd.read_csv(f"datamodules/{current_version}/{current_patch}/songList_temp.csv")

test_dict = json.load(open("testme.json"))

rankdata_by_level = {}
for i in range(20,27):
    rankdata_by_level[str(i)] = json.load(open(f"datamodules/in100RankData/{current_date}/rankdata_{i}.json"))
rankdata_by_level["27over"] = json.load(open(f"datamodules/in100RankData/{current_date}/rankdata_27over.json"))

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
