import streamlit as st
import re
import time
from app.manager import Table4AllManager


def launch():
    st.set_page_config(layout="centered", page_title="Table 4 All", page_icon="figures/basket.png")

    if "manager" not in st.session_state:
        st.session_state.manager = Table4AllManager()
    if "current_user_id" not in st.session_state:
        st.session_state.current_user_id = None
    if "current_user_type" not in st.session_state:
        st.session_state.current_user_type = None

    st.sidebar.title("Table 4 All")
    login_page = st.Page("gui/login.py", title="Log in & Register", icon=":material/login:")
    logout_page = st.Page("gui/logout.py", title="Log out", icon=":material/logout:")
    volunteer_page = st.Page("gui/volunteer_page.py", title="Volunteer Page")
    staff_page = st.Page("gui/staff_page.py", title="Staff Page")
    client_page = st.Page("gui/client_page.py", title="Client Page")
    user_id = st.session_state.current_user_id
    user_type = st.session_state.current_user_type
    if user_id:
        page = st.navigation({"Directory": [eval(f"{user_type}_page")], "Account": [logout_page]})
    else:
        page = st.navigation({"Account": [login_page]}) 

    page.run()

