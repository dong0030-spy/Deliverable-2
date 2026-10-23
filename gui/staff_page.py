import streamlit as st
import time
import re

user_id = st.session_state.current_user_id
manager = st.session_state.manager
user = manager.get_staff(user_id)
st.header(f"Welcome! {user.name}.")

food_name_pattern = r"^[A-Za-z]\w{2,}$"

stock, register_food, review_donations = st.tabs(["Stock", "Register Food", "Review Donations"])
with stock:
    st.subheader(f"Stock")
    for s in manager.storage:
        with st.container(border=True):
            color = ""
            text = ""
            if s.quantity == 0:
                color = "red"
                text = "NO STOCK"
            elif s.quantity <= 100:
                color = "yellow"
                text = "LOW STOCK"
            else:
                color = "green"
                text = "AVAILABLE"
            st.subheader(f"**{s.name}**")
            st.markdown(f'''
            ID: *{s.id}*

            Stock: :{color}[*{s.quantity}*]
            ''')
            st.markdown(f''':{color}[*{text}*]''', text_alignment="right")
        

with register_food:
    name = st.text_input("Food name", max_chars=30)
    quantity = st.number_input("Food quantity", min_value=0, max_value=10000)
    if st.button("Confirm"):
        if re.match(food_name_pattern, name):
            new_food = manager.register_new_food(name, quantity)
            st.success(f"Food {new_food.id} added successfullly!")
            time.sleep(3)
            st.rerun()
        else:
            st.error('''
            **Invalid name.**
            - Food name must be 3 characters or longer
            - Food name must begin with alpha characters
            ''')

@st.dialog("View Donation")
def view_donation(donation):
    st.subheader(f"Donation registration from client {donation.donor_id} ID: *{donation.id}*")
    for i, food_id in enumerate(donation.donation_list):
        food = manager.get_food(food_id)
        with st.container(border=True, key=f"Item {i}"):
            st.subheader(f"**{food.name}** *{food.id}*")
            st.write(f"Quantity: **{food.pending[donation.donor_id]["quantity"]}**")
            st.write(f"Received: **{food.pending[donation.donor_id]["received"]}**")
            st.write(f"Expiery date: *{food.pending[donation.donor_id]["expiery_date"]}*")
    st.write(f"Remarks: {donation.remarks}")
    btn = st.button("Confirm donation")
    if btn:
        btn = st.empty()
        manager.approve_donation(donation.id)
        st.success("Successfully approved donation.")
        time.sleep(2)
        st.rerun()

with review_donations:
    for i, donation in enumerate(manager.pending_donations):
        with st.container(border=True, key=f"Donation {i}"):
            if st.button(f"Donation by *{donation.donor_id}* ID: *{donation.id}*", width="stretch"):
                view_donation(donation)

