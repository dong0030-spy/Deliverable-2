import streamlit as st
import time

st.header("Log Out")
if st.button("Log out"):
    st.session_state.current_user_id = None
    st.session_state.current_user_type = None
    st.success("Successfully logged out!")
    time.sleep(2)
    st.rerun()