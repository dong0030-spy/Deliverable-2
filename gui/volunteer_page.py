import streamlit as st
import time
import re

user_id = st.session_state.current_user_id
manager = st.session_state.manager
user = manager.get_volunteer(user_id)
st.header(f"Welcome! {user.name}.")

receive_donation, = st.tabs(["Receive Donations"])

if "update_donation_pressed" not in st.session_state:
    st.session_state.update_donation_pressed = False

def reset_button():
    st.session_state.update_donation_pressed = False
@st.dialog("View Donation", on_dismiss=reset_button)
def view_donation(donation):
    st.subheader(f'''
    Donation registration from client {donation.donor_id} 
    ID: *{donation.id}*
    ''')
    for i, food_id in enumerate(donation.donation_list):
        food = manager.get_food(food_id)
        with st.container(border=True, key=f"Item {i}"):
            st.subheader(f"**{food.name}** *{food.id}*")
            st.write(f"To receive: **{food.pending[donation.donor_id]["quantity"] - food.pending[donation.donor_id]["received"]}**")
            st.write(f"Expiery date: *{food.pending[donation.donor_id]["expiery_date"]}*")
    st.write(f"Remarks: {donation.remarks}")
    if st.button("Update Donation", width="stretch", disabled=st.session_state.update_donation_pressed) or st.session_state.update_donation_pressed:
        st.session_state.update_donation_pressed = True
        with st.container(border=True):
            update_list = {}
            for food_id in donation.donation_list:
                food = manager.get_food(food_id)
                amount_received = st.number_input(food.name, min_value=1, max_value=food.pending[donation.donor_id]["quantity"] - food.pending[donation.donor_id]["received"], required=True)
                update_list[food_id] = amount_received
            st.warning("Only press the button if the donation is physically received.")
            if st.button("Receive Donation", width="stretch"):               
                manager.update_donation(donation.donor_id, update_list)
                st.success("Successfully updated donation.")
                time.sleep(2)
                st.rerun()

with receive_donation:
    for donation in manager.approved_donations:
        total = 0
        current = 0
        for food_id in donation.donation_list:
            food = manager.get_food(food_id)
            total += food.pending[donation.donor_id]["quantity"]
            current += food.pending[donation.donor_id]["received"]
        if total == current:
            manager.complete_donation(donation.id)
        else:
            with st.container(border=True):
                st.markdown(f'''
                Donation {donation.id}        
                Date: {donation.timestamp}
                ''')
                st.progress(current / total, f"Receive Progress: {int(current / total * 100)}%", 200)
                if st.button("Receive", width="stretch"):
                    view_donation(donation)
    