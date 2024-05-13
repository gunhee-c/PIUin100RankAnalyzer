from in100_utils import *

import streamlit as st
st.header("PIU in 100 data Analyzer")
st.write("This is a simple web app that analyzes the data from the PIU in 100 rank dataset.")
st.write("Currently the data is up to 05/09/2024")


find_user, single_player, two_player, update= st.tabs(["Find User", "Single Player Analysis", "Player comparison", "updates"])

with find_user:
    st.write("in this page you can search a user's name and ID")
    st.header("Find User")
    user_name = st.text_input("Enter the user's name")
    if user_name != "":
        #user_info = search_user(user_name)
        strs = print_search_user(user_name)
        for s in strs:
            st.write(s)
with single_player:
    st.write("This is the single player analysis page")
with two_player:
    st.write("This is the player comparison page")
with update:
    st.write("This is the update page")
