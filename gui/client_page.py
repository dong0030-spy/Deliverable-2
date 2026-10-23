import streamlit as st
import time

user_id = st.session_state.current_user_id
manager = st.session_state.manager
user = manager.get_client(user_id)
st.header(f"Welcome! {user.name}.")

if "new_food" not in st.session_state:
    st.session_state.new_food = None
if "foods" not in st.session_state:
    st.session_state.foods = []
if "donation" not in st.session_state:
    st.session_state.donation = None

food_name_pattern = r"^[A-Za-z]\w{2,}$"
@st.dialog("Add New Food")
def new_food():
    name = st.text_input("Food name", max_chars=30, live=True, type="search", placeholder="Search for food name")
    results = manager.search_food(name)
    food_list = {f"{f.name} {f.id}": f for f in results}
    for v in st.session_state.foods:
        try:
            food_list.pop(f"{v["obj"].name} {v["obj"].id}")
        except KeyError:
            pass
    food_choice = st.selectbox("Existing foods", food_list)
    quantity = st.number_input("Food quantity", min_value=1, max_value=10000)
    expiery_date = st.date_input("Expiery date", min_value="today")
    if st.button("Add Food"):
        if food_choice:
            food = food_list[food_choice]
            st.session_state.new_food = {"id": food.id, "quantity_to_add": quantity, "expiery_date": expiery_date.strftime("%d-%m-%Y")}
            st.rerun()
        else:
            st.warning("Please choose a food.")

dashboard, new_donation, donation_history = st.tabs(["Dashboard", "New Donation", "Donation History"])
with dashboard:
    st.subheader("Dashboard (WIP)")
    st.header("Clients helped: 67", text_alignment="center")

@st.dialog("Donation Guidelines")
def view_guidelines():
    st.write('''
    - All donations will be used for helping the client that are in need of food.
    - Donations are required to be delivered by the donor, any extra fees are not covered.
    - Upon donation approval, the donation cannot be cancelled.
    - Food expiery date must be at least 2 weeks long.
    ''')
pending_donation_count = 0

with donation_history:
    with st.container(border=True, key=f"Donation History"):
        st.header("Donation History")
        for d in manager.pending_donations:
            if d.donor_id == user_id:
                with st.container(border=True):
                    st.markdown(f'''
                    Donation {d.id}        
                    Date: {d.timestamp}         
                    Status: :yellow[{d.status.upper()}]
                    ''')
                pending_donation_count += 1
        for d in manager.approved_donations:
            if d.donor_id == user_id:
                with st.container(border=True):
                    st.markdown(f'''
                    Donation {d.id}        
                    Date: {d.timestamp}         
                    Status: :blue[{d.status.upper()}]
                    ''')
                pending_donation_count += 1
        for d in manager.completed_donations:
            if d.donor_id == user_id:
                with st.container(border=True):
                    st.markdown(f'''
                    Donation {d.id}        
                    Date: {d.timestamp}         
                    Status: :green[{d.status.upper()}]
                    ''')

with new_donation:
    if pending_donation_count == 0:
        if not st.session_state.donation:
            st.session_state.donation = manager.register_donation(user_id)
        donation = st.session_state.donation
        foods = st.session_state.foods
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button("New Food"):
                new_food()
        with col2:
            if st.button("View Guidelines"):
                view_guidelines()
        if st.session_state.new_food:
            foods.append(st.session_state.new_food)
            st.session_state.new_food = None
        for i, item in enumerate(foods):
            food = manager.get_food(item["id"])
            with st.container(border=True, key=f"Food {i}"):
                st.subheader(f"**{food.name}** *{food.id}*")
                st.write(f"In storage: **{food.quantity}**")
                st.write(f"Quantity: **{item["quantity_to_add"]}**")
                st.write(f"Expiery date: *{item["expiery_date"]}*")
        remarks = st.text_input("Remarks", max_chars=300, placeholder="Enter remarks such as storage requirements")
        btn = st.button("Confirm Donation", width="stretch")
        if btn and len(foods) > 0:
            btn = st.empty()
            donation_food_ids = []
            for item in foods:
                food = manager.get_food(item["id"])
                donation_food_ids.append(food.id)
                food.add_donation(manager, donation.donor_id, {"quantity": item["quantity_to_add"], "received": 0, "expiery_date": item["expiery_date"]})
            user.donation_history.append(donation.id)
            donation.add_items(manager, donation_food_ids, remarks)
            st.success("Donation added successfullly!")
            manager._save_data()
            foods.clear()
            time.sleep(2)
            st.rerun()
        elif btn and len(foods) == 0:
            st.error("No food was added, donation unsuccessful.")
    else:
        st.error("A pending donation is in process, new donation cannot be created")


