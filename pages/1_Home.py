"""
Home page - welcome and overview of available tools.
"""
import streamlit as st

from components.home_content import render_home_content
from utils.helpers import init_page

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

init_page()
render_home_content()
