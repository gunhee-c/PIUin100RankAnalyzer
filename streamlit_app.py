from in100_utils import *
from in100_utils_presentation import *
from streamlit_text import *

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random as rd


def gather_userdata(key_name):
    user_name, user_id = get_user_info(key_name)
    is_user_valid(user_name, user_id)
    if user_id == "": 
        user = return_user_with_name(user_name)
    else:
        user_name_full = user_name + " " + user_id
        user = return_user_with_name(user_name_full)
    st.write("You can filter the data by mode, level, song type, and version")
    mode, min_level, max_level, songtype_list, version_list = get_filter_values(key_name)
    #toggle_score, toggle_sort = get_score_and_sort("single")
    user_key = user["username"] + " " + user["userID"]    
    return user_key, mode, min_level, max_level, songtype_list, version_list


def gather_userdata_of_two(key_name):
    user_name1, user_id1 = get_user_info(key_name+"1")
    is_user_valid(user_name1, user_id1)
    user_name2, user_id2 = get_user_info(key_name+"2")
    is_user_valid(user_name2, user_id2)
    if user_id1 == "": 
        user1 = return_user_with_name(user_name1)
    else:
        user_name_full_1 = user_name1 + " " + user_id1
        user1 = return_user_with_name(user_name_full_1)
    if user_id2 == "":
        user2 = return_user_with_name(user_name2)
    else:
        user_name_full_2 = user_name2 + " " + user_id2
        user2 = return_user_with_name(user_name_full_2)
    
    st.write("You can filter the data by mode, level, song type, and version")
    mode, min_level, max_level, songtype_list, version_list = get_filter_values(key_name)
    #toggle_score, toggle_sort = get_score_and_sort("single")
    user_key1 = user1["username"] + " " + user1["userID"]
    user_key2 = user2["username"] + " " + user2["userID"]
    return user_key1, user_key2, mode, min_level, max_level, songtype_list, version_list

def main():
    main_text()


    find_user, single_player, two_player, update= st.tabs(["Find User & Song", "Single Player Analysis", "Player comparison", "updates"])

    with find_user:
        find_user_song_text()

        user_name = st.text_input("Enter the user's name")
        if user_name != "":
            #user_info = search_user(user_name)
            strs = print_search_user(user_name)
            for s in strs:
                st.write(s)
    with single_player:

        user_key, mode, min_level, max_level, songtype_list, version_list = gather_userdata("single")
        
        st.divider()
        data_pandas, count_user, achievement_rate, ranks, ranks_by_level = rankdata(user_key, mode = mode, levels = [min_level, max_level], songtype = songtype_list, version = version_list)
        
        count_user_with_level = {}
        for key in count_user.keys():
            count_user_with_level["lv " + str(key)] = count_user[key]
        st.write(str(count_user_with_level))
        st.dataframe(data_pandas)
        show_achievement(achievement_rate)
        show_rank(ranks)
        show_scatterplot(ranks_by_level)
        

    with two_player:

        user_key1, user_key2, mode, min_level, max_level, songtype_list, version_list = gather_userdata_of_two("two")
        st.divider()

        user_comparison, total_count_comparison, aggregated_dataframe = rankdata_compare(user_key1, user_key2, mode = mode, levels = [min_level, max_level], songtype = songtype_list, version = version_list)
        st.dataframe(aggregated_dataframe)
        show_user_comparison(user_comparison)
        show_total_count_comparison(total_count_comparison)
    with update:
        st.write("05/13: First version of the app is released")
        st.write("05/16: Data update")



def expander_with_list(expander_name, user_name, expand = True):
    with st.expander(expander_name):
        strs = print_search_user(user_name, exact = True)
        for s in strs:
            st.write(s)

def get_score_and_sort(key_name):
    col1, col2 = st.columns(2)
    toggle_score, toggle_sort = True, False
    if toggle_score:
        score_toggle = "Sort by score"
    else:
        score_toggle = "Sort by rank"
    if toggle_sort:
        sort_toggle = "Sort by level first"
    else:
        sort_toggle = "Sort Everything"
    with col1:
        toggle_score = st.toggle(score_toggle, key = key_name + "toggle_score", value = True)
    with col2:
        toggle_sort = st.toggle(sort_toggle, key = key_name + "toggle_sort", value = False)
    sortby = "score"
    if toggle_score == False:
        sortby = "rank"
    return sortby, toggle_sort

def is_user_valid(username, userID):
    if username == "":
        st.error("Please enter the user's name")
        st.stop()
    list_of_users = list((search_user(username, exact = True)).values())
    if len(list_of_users) == 0:
        st.error("User is not found in ranking data")
        st.stop()
    if userID == "":
        if len(list_of_users[0]) > 1:
            st.error("There are multiple users with the same name. Please provide the userID")
            expander_with_list("Users with the same name", username)
            st.stop()

        user = return_user_with_name(username)
        st.success("User is valid")
    else:
        user = return_user_with_name(username + " " + userID)
        if user == None:
            st.error("User ID is invalid. Please provide the correct ID")
            st.stop()
        else:
            st.success("User is valid")
    return user

def get_user_info(key_name):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("user's name", key=key_name + "NAME", value="")
    with col2:
        user_id = st.text_input("user's ID (you can skip #)", key= key_name +"ID", value="")
    st.write("if your ID is unique among the users with the same name, you can leave the ID blank")
    if user_id != "":
        if user_id[0] != "#":
            user_id = "#" + user_id
    return user_name, user_id

def get_filter_values(key_name):
    mode, min_level, max_level = three_filter_inputs(key_name)
    songtype_list = checkboxes_songtype(key_name)
    version_list = checkboxes_version(key_name)
    return mode, min_level, max_level, songtype_list, version_list

def checkboxes_songtype(key_name):
    st.write("Choose the song type")
    col1, col2, col3, col4 = st.columns(4,gap="small")

    songtypes = {
        "Arcade": col1.checkbox("Arcade", value=True, key=f"{key_name}_Arcade"),
        "Remix": col2.checkbox("Remix", value=True, key=f"{key_name}_Remix"),
        "Full Song": col3.checkbox("Full Song", value=True, key=f"{key_name}_Full Song"),
        "Short Cut": col4.checkbox("Short Cut", value=True, key=f"{key_name}_Short Cut")
    }
    
    # Return the keys of the versions where the checkbox is checked
    return [songtype for songtype, checked in songtypes.items() if checked]

def checkboxes_version(key_name):
    st.write("Choose the version (song)")
    col1, col2, col3 = st.columns(3, gap="small")
    
    # Initialize checkboxes and collect their statuses in a dictionary
    versions = {
        "PHOENIX": col1.checkbox("PHOENIX", value=True, key=f"{key_name}_PHOENIX"),
        "XX": col2.checkbox("XX", value=True, key=f"{key_name}_XX"),
        "OLD": col3.checkbox("OLD", value=True, key=f"{key_name}_OLD")
    }
    
    # Return the keys of the versions where the checkbox is checked
    return [version for version, checked in versions.items() if checked]

def three_filter_inputs(key_name):
    # Create a three-column layout
    col1, col2, col3 = st.columns(3)
    # SelectBox for Mode in the first column
    with col1:
        mode = st.selectbox(
            'Choose the game mode:',
            ('Full', 'Single', 'Double'),
            index = 0,
            key = key_name + "mode"
        )

    # Numeric input for minimum level in the second column
    with col2:
        min_level = st.number_input(
            'Minimum Level',
            min_value=20,  # Minimum level possible
            max_value=28,  # Maximum level possible
            value=20,  # Default value
            step=1,  # Increment step
            key = key_name + "min_level"
        )

    # Numeric input for maximum level in the third column
    with col3:
        max_level = st.number_input(
            'Maximum Level',
            min_value=20,  # Minimum level possible
            max_value=28,  # Maximum level possible
            value=28,  # Default value
            step=1,  # Increment step
            key = key_name + "max_level"
        )

    # Validate input to ensure max_level is not less than min_level
    if max_level < min_level:
        st.error('Maximum level should be greater than or equal to minimum level.')

    return mode, min_level, max_level


if __name__ == "__main__":
    main()

    