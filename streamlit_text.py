import streamlit as st
def main_text():
    st.header("PIU in 100 data Analyzer")
    st.write("This is a simple web app that analyzes the data from the PIU in 100 rank dataset.")
    st.write("Currently the data is up to 06/12/2024")

def find_user_song_text():
    st.write("in this page you can search a user's name and ID")
    st.header("Find User")
    st.write("This will provide user's ID and his/her ranking data")
    st.write("All users including your response will be shown")
    st.write("If there are other users with same username, you need to provide your userID to get your data.")

def single_user_text():
    st.write("in this page you can search a user's name and ID")
    st.header("Single User")
    st.write("This will provide user's ID and his/her ranking data")
    st.write("You can search only one user")