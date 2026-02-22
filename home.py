"""
Main entry point. Run with: streamlit run home.py
"""
import streamlit as st

from components.home_content import render_home_content
from utils.helpers import init_page

st.set_page_config(page_title="Bioinformatics Portal", page_icon="🧬", layout="wide")

init_page()
render_home_content()
