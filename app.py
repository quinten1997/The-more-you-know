import streamlit as st
from backend import run_app_logic

st.set_page_config(page_title="Nearby Explorer", layout="wide")
run_app_logic()
