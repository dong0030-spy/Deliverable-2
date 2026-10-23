import streamlit as st
import re
import time

username_pattern = r"^[A-Za-z]\w{7,}$"
password_pattern = r"^(\d+|[A-Z]+|[a-z]+|\W+){12,}$"

manager = st.session_state.manager
log_in, register = st.tabs(["Log In", "Register"])
with log_in:
    term = st.text_input("Username or User ID", placeholder="Enter username or user ID", max_chars=30)
    pwd = st.text_input("Password", placeholder="Enter password", max_chars=30, type="password")
    if st.button("Log in"):
        user = manager.get_client(term)
        staff = manager.get_staff(term)
        volunteer = manager.get_volunteer(term)
        if user or staff or volunteer:
            if user and manager.check_password(user, pwd):
                st.session_state.current_user_id = user.id 
                st.session_state.current_user_type = user.type_name
                st.success(f"Logging in as client {user.id}")
            elif staff and manager.check_password(staff, pwd):
                st.session_state.current_user_id = staff.id
                st.session_state.current_user_type = staff.type_name
                st.success(f"Logging in as staff {staff.id}")
            elif volunteer and manager.check_password(volunteer, pwd):
                st.session_state.current_user_id = volunteer.id
                st.session_state.current_user_type = volunteer.type_name
                st.success(f"Logging in as volunteer {volunteer.id}")
            else:
                st.error("Invalid credentials. Username/ID does not exist or incorrect password.")
            time.sleep(2)
            st.rerun()
        else:
            st.error("Invalid credentials. Username/ID does not exist or incorrect password.")

        

with register:
    username = st.text_input("Username", placeholder="Enter username", max_chars=30)
    pwd = st.text_input("Password ", placeholder="Enter password", max_chars=30, type="password")
    if st.button("Register"):
        username_check = re.match(username_pattern, username)
        pwd_check = re.match(password_pattern, pwd)
        if username_check and pwd_check:
            new_client = manager.register_new_client(username, pwd)
            st.success(f"Successfully registered as client {new_client.id}!")
            time.sleep(2)
            st.rerun()
        elif not username_check:
            st.error('''
            **Please input a valid username.**
            - Name can only be alpha-numeric 
            - First character must not be a digit
            - Username must be 8 characters or longer
            ''')
        else:
            st.error('''
            **Please input a valid password.**
            - Password must contain at least a uppercase letter, a lowercase letter, a number and a special character
            - Password length must be 12 characters or longer
            ''')
