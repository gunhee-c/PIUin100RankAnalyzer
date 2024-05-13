from in100_utils import *

import streamlit as st
st.header("PIU in 100 data Analyzer")
st.write("This is a simple web app that analyzes the data from the PIU in 100 rank dataset.")
st.write("Currently the data is up to 05/09/2024")


readme, single_player, two_player, update= st.tabs(["Readme", "Single Player Analysis", "Player comparison", "updates"])

with readme:
    st.write("리드미는나중에")
with single_player:
    st.write("This is the single player analysis page")
with two_player:
    st.write("This is the player comparison page")
with update:
    st.write("This is the update page")
