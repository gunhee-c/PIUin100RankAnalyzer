import requests
from bs4 import BeautifulSoup
import re
import json
import os


current_version = "PHOENIX"
current_patch = "2.0.0"
url_substr1 = "https://piugame.com/leaderboard/over_ranking.php?lv="
url_substr2 = "&search=&&page="
num_pages_by_level = {"20": 19, "21": 19, "22": 14, "23": 10, "24": 7, "25": 4, "26": 2, "27over": 1}

maxpage_ucs = 45


def extract_soup_from_URL(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

#버전을 숫자로 변환, PHOENIX, XX, PRIME, FIESTA, NX, 1st - Zero
def convert_int_into_version(num):
    if num<=14:
        return "1st - Zero"
    elif num <=17:
        return "NX - NXA"
    elif num <= 21:
        return "FIESTA - FIESTA 2"
    elif num <= 23:
        return "PRIME - PRIME 2"
    elif num <= 24:
        return "XX"
    else:
        return "PHOENIX"

#{index, song, composer, bpm, version}의 리스트 반환
def extract_ucs_list(soup):
    ans = []
    ucs_index_list = []
    ucs_song_list = []
    ucs_composer_list = []
    ucs_bpm_list = []
    ucs_version_list = []
    for a in soup.find_all("td", class_ = "w_no2"):
        ucs_index_list.append(a.text.strip())
    for a in soup.find_all("p", class_ = "t1"):
        ucs_song_list.append(a.text.strip())
    for a in soup.find_all("p", class_ = "t2"):
        ucs_composer_list.append(a.text.strip())
    for a in soup.find_all("td", class_ = "w_bpm"):
        ucs_bpm_list.append(a.text.strip())
    for a in soup.find_all("td", class_ = "w_version"):
        #print(a)
        a_str = str(a)
        version_num = re.search(r'version/(.*).png', a_str).group(1)
        ucs_version_list.append(convert_int_into_version(int(version_num)))
    for i in range(len(ucs_index_list)):
        ans.append({"index": ucs_index_list[i], "song": ucs_song_list[i], "composer": ucs_composer_list[i], "bpm": ucs_bpm_list[i], "version": ucs_version_list[i]})
    return ans

#각 페이지의 링크를 추출, {songname: URL}의 딕셔너리 반환
def extract_page_links(soup):
    subURLs = []
    songnames = []
    for a in soup.find_all("a", {'class': "in flex vc wrap"}):
        subURLs.append("https://piugame.com/leaderboard/" + a['href'])
    for b in soup.find_all("div", {'class': "songName_w"}):
        songnames.append(b.text)
    dict_zip = dict(zip(songnames, subURLs))
    return dict_zip

# 레벨 링크 추출에 사용되는 함수// 각 레벨 별 URL 링크들 반환
def construct_URL_list(level):
    URL_list = []
    for i in range(1, num_pages_by_level[level]+1):
        URL_list.append(url_substr1 + level + url_substr2 + str(i))
    return URL_list

#각 레벨별로 모든 페이지의 링크를 추출, {songname: URL}의 딕셔너리 반환
def extract_all_page_links(level):
    print("Extracting all page links for level " + level + "...")
    URL_list = construct_URL_list(level)
    len_url_list = len(URL_list)
    all_subURLs = {}
    count = 0
    for URLs in URL_list:
        print("current progress: " + str(count+1) + "/" + str(len_url_list))
        count += 1
        soup = extract_soup_from_URL(URLs)
        all_subURLs.update(extract_page_links(soup))
    return all_subURLs

if __name__ == "__main__":
    total_ucs = []
    #for i in range(1,maxpage_ucs + 1):
    for i in range(1, 2):
        print(i)
        current_url = 'https://ucs.piugame.com/sample_download/list.php?search=&&page=' + str(i)
        ucs_soup = extract_soup_from_URL(current_url)
        ucs_list = extract_ucs_list(ucs_soup)
        for j in ucs_list:
            total_ucs.append(j)

    subURL_20 = extract_all_page_links("20")
    subURL_21 = extract_all_page_links("21")
    subURL_22 = extract_all_page_links("22")
    subURL_23 = extract_all_page_links("23")
    subURL_24 = extract_all_page_links("24")
    subURL_25 = extract_all_page_links("25")
    subURL_26 = extract_all_page_links("26")
    subURL_27over = extract_all_page_links("27over")
    subURLs = {"20": subURL_20, "21": subURL_21, "22": subURL_22, "23": subURL_23, "24": subURL_24, "25": subURL_25, "26": subURL_26, "27over": subURL_27over}


    current_path = "datamodules/"+current_version+"/"+current_patch
    os.makedirs(current_path, exist_ok=True)
    current_path_songinfo = os.path.join(current_path, 'arcade_song_metadata.json')
    current_patch_linkinfo = os.path.join(current_path, 'subURLs_list.json')

    #with open(current_path_songinfo, 'w') as f:
    #    json.dump(total_ucs, f)
    with open(current_patch_linkinfo, 'w') as f:
        json.dump(subURLs, f)


