import requests
from bs4 import BeautifulSoup
import re
import json
import os
import pandas as pd
#랭킹 데이터 형성

class RankData:
    def __init__(self, song, mode, level, username, userid, score, rank):
        self.song = song
        self.mode = mode
        self.level = level
        self.username = username
        self.userid = userid
        self.score = score
        self.rank = rank
        self.scorestr = self.score_str()
    def __str__(self):
        #return f"{self.song} {self.mode} {self.level}: {self.username}({self.userid}) score: {self.score}, rank: {self.rank}"
        return f"{self.username}: rank: {self.rank}, score: {self.scorestr}"
    def score_str(self):
        return str(self.score//1000) + "," + str(self.score%1000)
    def to_dict(self):
        return {"song": self.song, "mode": self.mode, "level": self.level, "username": self.username, "userid": self.userid, "score": self.score, "rank": self.rank}
    
def RankData_to_json(rankdata):
    instances_dict = [instance.to_dict() for instance in rankdata]
    json_string = json.dumps(instances_dict, indent=4)
    return json_string

#son, mode, level 반환
def get_songinfo(soup):
    song = soup.find("div", class_ = "songName_w").text
    mode_raw = str(soup.find("div", class_ = "level_w").find("div", class_ = "tw"))
    mode_alpha = re.search(r'full/(.*)_text', mode_raw).group(1)
    if mode_alpha == "d": mode = "Double"
    elif mode_alpha == "s": mode = "Single"
    level_raw = soup.find("div", class_ = "level_w").find_all("div", class_ = "imG")
    level_raw_1 = str(level_raw[0])
    level_raw_2 = str(level_raw[1])
    level_1 = re.search(r'num_(.*)\.png', level_raw_1).group(1)
    level_2 = re.search(r'num_(.*)\.png', level_raw_2).group(1)
    level = int(level_1 + level_2)
    return song, mode, level

#rank_to_int 하위 함수
def has_medal(soup):
    if soup.find("span", class_ = "medal_wrap") == None:
        return False
    else:
        return True

def extract_soup_from_URL(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

#등수 정보를 정수로 변환
def rank_to_int(soup):
    if has_medal(soup):
        medaltext = str(soup.find("img"))
        medal = re.search(r'img/(.*)medal', medaltext).group(1)
        if medal == "gold":
            return 1
        elif medal == "silver":
            return 2
        elif medal == "bronze":
            return 3
    else:
        return int(soup.find("div", class_ = "num").text)

#유저 랭킹 정보의 리스트 반환
def get_rank_list(soup):
    lst = soup.find("div", class_ = "rangking_list_w").find_all("li")
    rank_list = []
    for i in range(len(lst)):
        username = lst[i].find("div", class_ = "profile_name en").text
        userID = lst[i].find("div", class_ = "profile_name st1 en").text
        score = int(lst[i].find("div", class_ = "score").text.replace(",", ""))
        rank = rank_to_int(lst[i])
        rank_list.append((username, userID, rank, score))
    return rank_list

def get_rankdata_from_soup(soup):
    songinfo = get_songinfo(soup)
    print(songinfo)
    rank_list = get_rank_list(soup)
    rank_data = []
    for i in range(len(rank_list)):
        rank_data.append(RankData(songinfo[0], songinfo[1], songinfo[2], rank_list[i][0], rank_list[i][1], rank_list[i][3], rank_list[i][2]))
    return rank_data

def get_rankdata_by_level(subURLs, level_category):
    rankdata_by_level = {}
    len_data = len(subURLs[level_category])
    count = 1
    for URLs in subURLs[level_category]:
        print(f"{count}/{len_data}")
        count += 1
        soup = extract_soup_from_URL(subURLs[level_category][URLs])
        song, mode, level = get_songinfo(soup)
        songID = song + " " + mode + str(level)
        rankdata_by_level[songID] = get_rankdata_from_soup(soup)

    return rankdata_by_level

def save_rankdata_by_level(file_path, rankdata_by_level, level):
    json_total = {}
    for item in rankdata_by_level:
        json_total[item] = []
        for instance in rankdata_by_level[item]:
            json_total[item].append(instance.to_dict())
    with open(f"{file_path}/rankdata_{level}.json", "w") as file:
        json.dump(json_total, file)
        #json.dump(json_total, file, cls=RankDataEncoder)


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


if __name__ == "__main__":

    current_version = "PHOENIX"
    current_patch = "2.0.0"
    current_date = "2024.06.19"
    with open(f"datamodules/{current_version}/{current_patch}/subURLs_list.json", "r") as file:
        subURLs = json.load(file)
    #todo implement songlist here
    songlist = pd.read_csv(f"datamodules/{current_version}/{current_patch}/songList_temp.csv")
    current_path = "datamodules/in100RankData/"+current_date
    os.makedirs(current_path, exist_ok=True)
    for level in subURLs:
        rankdata_by_level = get_rankdata_by_level(subURLs, level)
        save_rankdata_by_level(current_path, rankdata_by_level, level)
