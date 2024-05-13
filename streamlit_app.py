from in100_utils import *

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
    st.header("PIU in 100 data Analyzer")
    st.write("This is a simple web app that analyzes the data from the PIU in 100 rank dataset.")
    st.write("Currently the data is up to 05/09/2024")


    find_user, single_player, two_player, update= st.tabs(["Find User", "Single Player Analysis", "Player comparison", "updates"])

    with find_user:
        st.write("in this page you can search a user's name and ID")
        st.header("Find User")
        st.write("This will provide user's ID and his/her ranking data")
        st.write("All users including your response will be shown")
        st.write("If there are other users with same username, you need to provide your userID to get your data.")
        user_name = st.text_input("Enter the user's name")
        if user_name != "":
            #user_info = search_user(user_name)
            strs = print_search_user(user_name)
            for s in strs:
                st.write(s)
    with single_player:
        '''
        st.write("This is the single player analysis page")
        st.write("Enter the user that you want to analyze")
        user_name, user_id = get_user_info("single")
        is_user_valid(user_name, user_id)
        if user_id == "": 
            user = return_user_with_name(user_name)
        else:
            user_name_full = user_name + " " + user_id
            user = return_user_with_name(user_name_full)
        st.write("You can filter the data by mode, level, song type, and version")
        mode, min_level, max_level, songtype_list, version_list = get_filter_values("single")
        #toggle_score, toggle_sort = get_score_and_sort("single")
        user_key = user["username"] + " " + user["userID"]
        '''
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
    with update:
        st.write("This is the update page")



def show_achievement(achievements):
    levels = list(achievements.keys())
    achievement_values_raw = list(achievements.values())
    achievement_values = []
    for item in achievement_values_raw:
        achievement_values.append(item*100)

    chart_type = st.selectbox('Select Chart Type', ['Bar Chart', 'Line Chart'])
    max_achievement = max(achievement_values)
    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == 'Bar Chart':
        ax.bar(levels, achievement_values, color='skyblue')
        plt.xlabel('Levels')
        plt.ylabel('Achievement (%)')
        plt.title('Achievement by Level')
        ax.set_ylim(0, max_achievement*1.2)  # Set y-axis to show scale from 0 to 1
    elif chart_type == 'Line Chart':
        ax.plot(levels, achievement_values, marker='o', linestyle='-', color='deepskyblue')
        plt.xlabel('Levels')
        plt.ylabel('Achievement (%)')
        plt.title('Achievement by Level')
        ax.set_ylim(0, max_achievement*1.2)  # Set y-axis to show scale from 0 to 1
        plt.grid(True)

    # Use Streamlit to render the figure
    st.pyplot(fig)

def show_rank(ranking_list):
    # Create a figure for the histogram
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(ranking_list, bins=range(1, 101, 10), edgecolor='black')  # Bins represent intervals of 10

    ax.set_title('Distribution of Rankings')
    ax.set_xlabel('Rankings (1-100)')
    ax.set_ylabel('Frequency')
    ax.set_xticks(range(0, 101, 10))  # Adjust the x-ticks for better visualization

    # Display the plot in Streamlit
    st.pyplot(fig)

def show_scatterplot(ranks_by_level):
    # Create a figure for the scatter plot
    fig, ax = plt.subplots(figsize=(6, 4))
    noise_strength = 0.2
    for category, values in ranks_by_level.items():
        categories = []
        for i in range(len(values)):
            categories.append(category + rd.uniform(-noise_strength, noise_strength))
        ax.scatter(categories, values, label=category, s=20)

    ax.set_title('Ranking by Level')
    ax.set_xlabel('Level')
    ax.set_ylabel('Rank')
    ax.legend(title='Levels', loc='upper right', bbox_to_anchor=(1.3, 1))
    # Display the plot in Streamlit
    st.pyplot(fig)



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
        st.header("User is found")
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
    st.write("you can skip # in userID")
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

    