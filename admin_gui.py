import streamlit as st
from admin import admin_login, add_nominee, get_nominee_list
from admin_count_functions import get_top3_nominees, individual_nominee_vote
import pandas as pd


st.set_page_config(page_title="Admin Dashboard", layout="wide")
def admin_login_ui():
    st.title("Admin Login")

    admin_email = st.text_input("Enter Admin Email:")
    admin_password = st.text_input("Enter Admin Password:", type='password')

    if st.button("Login"):
        if admin_login(admin_email, admin_password):
            st.session_state.logged_in = True
            return True
        else:
            st.error("Invalid credentials. Please try again.")
    return False

def add_nominee_ui():
    st.title("Add Nominee")

    nominee_name = st.text_input("Enter Nominee Name:")
    nominee_party = st.text_input("Enter Nominee Party:")

    if st.button("Add Nominee"):
        if nominee_name and nominee_party:
            if add_nominee(nominee_name, nominee_party):
                st.success(f"Nominee {nominee_name} from {nominee_party} added successfully!")
            else:
                st.error(f"Nominee {nominee_name} already exists.")
        else:
            st.warning("Please provide both nominee name and party.")

def view_nominee_list_ui():
    st.title("Nominee List")
    
    nominee_data = get_nominee_list()
    if nominee_data:
        nominee_data_adjusted = []
        for nominee_id, name, party in nominee_data:
            nominee_data_adjusted.append([nominee_id, name, party])
        headers = ["Nominee ID", "Nominee Name", "Nominee Party"]
        df_nominee_list = pd.DataFrame(nominee_data_adjusted, columns=headers)
        st.table(df_nominee_list)  
    else:
        st.warning("No nominees found.")

def top_3_nominees_ui():
    st.title("Top 3 Nominees")

    top_3 = get_top3_nominees()
    
    if top_3:
        top_3_list = []
        for i, (nominee_id, nominee_name, nominee_party, total_votes) in enumerate(top_3, start=1):
            top_3_list.append([i, nominee_name, nominee_party, total_votes])


        headers = ["Position","Nominee Name", "Nominee Party", "Total Votes"]
        df_top_3 = pd.DataFrame(top_3_list, columns=headers)
        st.table(df_top_3)
    else:
        st.warning("No data found.")

def individual_nominee_vote_ui():
    st.title("Individual Nominee Vote Count")
    
    nominee_id = st.text_input("Enter Nominee ID:", value="1") 
    if nominee_id:
        try:
            nominee_id = int(nominee_id) 
            if nominee_id > 0:
                result = individual_nominee_vote(nominee_id)
                if result:
                    result_data=[]
                    result_data.append([result[0], result[1], result[2], result[3]])
                    headers=["Nominee ID", "Nominee Name", "Nominee Party", "Total Votes"]
                    df_result = pd.DataFrame(result_data,columns=headers)
                    st.table(df_result)
                else:
                    st.warning("No votes found for the selected nominee.")
            else:
                st.warning("Please enter a valid positive number for Nominee ID.")
        except ValueError:
            st.warning("Please enter a valid numeric Nominee ID.")

def admin_dashboard():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.session_state.logged_in = False
        login=admin_login_ui()
        if login:
            st.rerun()
    else:
        option = st.selectbox("Select an Option:", ["Add Nominee", "View Nominee List", "Top 3 Nominees", "Individual Nominee Vote Count","Logout"])

        if option == "Logout":
            st.session_state.logged_in = False
            st.rerun()
        elif option == "Add Nominee":
            add_nominee_ui()
        elif option == "View Nominee List":
            view_nominee_list_ui()
        elif option == "Top 3 Nominees":
            top_3_nominees_ui()
        elif option == "Individual Nominee Vote Count":
            individual_nominee_vote_ui()

if __name__ == "__main__":
    admin_dashboard()
