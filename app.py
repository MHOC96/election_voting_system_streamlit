import pandas as pd
import streamlit as st

from admin import add_nominee, admin_login, get_nominee_list
from admin_count_functions import get_top3_nominees, individual_nominee_vote
from voter import get_voter_details, voter_vote

st.set_page_config(page_title="Election Voting System", layout="wide")


def voter_portal():
    st.title("Online Voting System")

    if "voter_verified" not in st.session_state:
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
                            "nic": nic_number,
                            "name": voter_name,
                            "district": district,
                            "electorate": electorate,
                        }
                        st.rerun()
                    else:
                        st.warning("Details do not match the database.")
    else:
        st.subheader("Nominee List")
        nominees = get_nominee_list()
        if nominees:
            st.table(
                pd.DataFrame(nominees, columns=["Nominee ID", "Name", "Party"])
            )
            nominee_id = st.selectbox(
                "Select Nominee ID to Vote", options=[n[0] for n in nominees]
            )

            if st.button("Submit Vote"):
                voter = st.session_state.voter_details
                result = voter_vote(
                    voter["nic"],
                    voter["name"],
                    voter["district"],
                    voter["electorate"],
                    nominee_id,
                )
                if "successfully" in result:
                    st.success(result)
                else:
                    st.error(result)

            if st.button("Logout"):
                st.session_state.voter_verified = False
                st.session_state.voter_details = {}
                st.rerun()
        else:
            st.warning("No nominees found.")


def admin_login_ui():
    st.title("Admin Login")

    admin_email = st.text_input("Enter Admin Email:")
    admin_password = st.text_input("Enter Admin Password:", type="password")

    if st.button("Login"):
        if admin_login(admin_email, admin_password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")


def add_nominee_ui():
    st.title("Add Nominee")

    nominee_name = st.text_input("Enter Nominee Name:")
    nominee_party = st.text_input("Enter Nominee Party:")

    if st.button("Add Nominee"):
        if nominee_name and nominee_party:
            if add_nominee(nominee_name, nominee_party):
                st.success(
                    f"Nominee {nominee_name} from {nominee_party} added successfully!"
                )
            else:
                st.error(f"Nominee {nominee_name} already exists.")
        else:
            st.warning("Please provide both nominee name and party.")


def view_nominee_list_ui():
    st.title("Nominee List")

    nominee_data = get_nominee_list()
    if nominee_data:
        df = pd.DataFrame(
            nominee_data, columns=["Nominee ID", "Nominee Name", "Nominee Party"]
        )
        st.table(df)
    else:
        st.warning("No nominees found.")


def top_3_nominees_ui():
    st.title("Top 3 Nominees")

    top_3 = get_top3_nominees()
    if top_3:
        rows = [
            [i, name, party, votes]
            for i, (_, name, party, votes) in enumerate(top_3, start=1)
        ]
        st.table(
            pd.DataFrame(
                rows,
                columns=["Position", "Nominee Name", "Nominee Party", "Total Votes"],
            )
        )
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
                    st.table(
                        pd.DataFrame(
                            [list(result)],
                            columns=[
                                "Nominee ID",
                                "Nominee Name",
                                "Nominee Party",
                                "Total Votes",
                            ],
                        )
                    )
                else:
                    st.warning("No votes found for the selected nominee.")
            else:
                st.warning("Please enter a valid positive number for Nominee ID.")
        except ValueError:
            st.warning("Please enter a valid numeric Nominee ID.")


def admin_portal():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.logged_in = False
        admin_login_ui()
        return

    option = st.selectbox(
        "Select an Option:",
        [
            "Add Nominee",
            "View Nominee List",
            "Top 3 Nominees",
            "Individual Nominee Vote Count",
            "Logout",
        ],
    )

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


def main():
    st.sidebar.title("Election Voting System")
    page = st.sidebar.radio("Navigate", ["Voter Portal", "Admin Dashboard"])

    if page == "Voter Portal":
        voter_portal()
    else:
        admin_portal()


if __name__ == "__main__":
    main()
