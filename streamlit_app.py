from in100_utils import *

import streamlit as st
st.header("PIU in 100 data Analyzer")
st.write("This is a simple web app that analyzes the data from the PIU in 100 rank dataset.")
st.write("Currently the data is up to 05/09/2024")


main_tabs = st.tabs["Readme", "Single Player Analysis", "Player comaparison", "updates"]

if main_tabs == "Readme":
    st.write("리드미는나중에")
elif main_tabs == "Single Player Analysis":
    st.write("This is the single player analysis page")
elif main_tabs == "Player comaparison":
    st.write("This is the player comparison page")
elif main_tabs == "updates":
    st.write("This is the update page")
