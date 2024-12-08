import streamlit as st
from voter import get_voter_details, voter_vote
from admin import get_nominee_list
import pandas as pd

st.set_page_config(page_title="Voting System", layout="wide")

def main():
    st.title("Online Voting System")
    if 'voter_verified' not in st.session_state:
        st.session_state.voter_verified = False

    if not st.session_state.voter_verified:
        nic_number = st.text_input("Enter your NIC Number")
        if nic_number:
            voter_details, error = get_voter_details(nic_number)
            if error:
                st.warning(error)
            else:
                voter_name = st.text_input("Full Name (as in NIC)")
                district = st.text_input("Electoral District")
                electorate = st.text_input("Electorate")

                if st.button("Verify"):
                    if (voter_name, district, electorate) == voter_details:
                        st.session_state.voter_verified = True
                        st.session_state.voter_details = {
                            'nic': nic_number, 'name': voter_name, 
                            'district': district, 'electorate': electorate
                        }
                        st.success("Verification successful! Proceed to vote.")
                    else:
                        st.warning("Details do not match the database.")
    else:
        st.subheader("Nominee List")
        nominees = get_nominee_list()
        if nominees:
            st.table(pd.DataFrame(nominees, columns=["Nominee ID", "Name", "Party"]))
            nominee_id = st.selectbox("Select Nominee ID to Vote", options=[n[0] for n in nominees])

            if st.button("Submit Vote"):
                voter = st.session_state.voter_details
                result = voter_vote(voter['nic'], voter['name'], voter['district'], voter['electorate'], nominee_id)
                if "successfully" in result:
                    st.success(result)
                else:
                    st.error(result)
            if st.button("Logout"):
                st.session_state.voter_verified = False
                st.session_state.voter_details = {}

if __name__ == "__main__":
    main()
