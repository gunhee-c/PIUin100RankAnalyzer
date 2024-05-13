from in100_utils import *

import streamlit as st

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
        st.write("This is the single player analysis page")
        st.write("Enter the user that you want to analyze")
        user_name, user_id = get_user_info("single")
        st.write("User name: ", user_name) 
        st.write("User ID: ", user_id)
        is_user_valid(user_name, user_id)
        if user_id == "": 
            st.header("User is found")
            user = return_user_with_name(user_name)
        else:
            st.header("ID is written")
            user_name_full = user_name + " " + user_id
            user = return_user_with_name(user_name_full)
        st.write("You can filter the data by mode, level, song type, and version")
        mode, min_level, max_level, songtype_list, version_list = get_filter_values("single")

    with two_player:
        st.write("This is the player comparison page")
    with update:
        st.write("This is the update page")

def expander_with_list(expander_name, user_name, expand = True):
    with st.expander(expander_name):
        strs = print_search_user(user_name, exact = True)
        for s in strs:
            st.write(s)


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
        user_name = st.text_input("Enter the user's name", key=key_name + "NAME", value="")
    with col2:
        user_id = st.text_input("Enter the user's ID", key= key_name +"ID", value="")
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
    with col1: 
        st.checkbox("Arcade", value=True, key=key_name+"Arcade")
    with col2:
        st.checkbox("Remix", value=True, key=key_name+"Remix")
    with col3:
        st.checkbox("Full Song", value=True, key=key_name+"Full Song")
    with col4:
        st.checkbox("Short cut", value=True, key=key_name+"Short cut")
    checkbox_list = []
    if col1:
        checkbox_list.append("Arcade")
    if col2:
        checkbox_list.append("Remix")
    if col3:
        checkbox_list.append("Full Song")
    if col4:
        checkbox_list.append("Short cut")

    return checkbox_list

def checkboxes_version(key_name):
    st.write("Choose the version(song)")
    col1, col2, col3 = st.columns(3,gap="small")
    with col1: 
        st.checkbox("PHOENIX", value=True, key=key_name+"PHOENIX")
    with col2: 
        st.checkbox("XX", value=True, key=key_name+"XX")
    with col3:
        st.checkbox("OLD", value=True, key=key_name+"OLD")
    checkbox_list = []
    if col1:
        checkbox_list.append("PHOENIX")
    if col2:
        checkbox_list.append("XX")
    if col3:
        checkbox_list.append("OLD")
    return checkbox_list

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

    