import streamlit as st

page_style = f"""
<style>
[data-testid="stSidebarHeader"] {{
background: rgba(6,0,0,0);
}}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)