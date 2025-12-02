import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Repair Dashboard", layout="wide")

# --- Authentication Setup ---
names = ["Admin User", "Viewer User"]
usernames = ["admin", "viewer"]
passwords = {"admin": "admin123", "viewer": "viewer123"}

authenticator = Authenticate(names, usernames, passwords, "repair_dashboard_cookie", "abcdef", cookie_expiry_days=1)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")

    # Initialize session state dataframe
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=[
                "Server",
                "Depot Name",
                "Fleet Number",
                "Registration",
                "Issue",
                "Priority",
                "Comments",
                "Status",
            ]
        )

    st.title("Repair Dashboard")

    # -------- ADMIN SECTION --------
    if username == "admin":
        st.subheader("Upload Excel File to Append Data")
        uploaded_file = st.file_uploader("Upload Excel (.xlsx) file", type=["xlsx"])
        if uploaded_file is not None:
            uploaded_df = pd.read_excel(uploaded_file)
            st.session_state.df = pd.concat([st.session_state.df, uploaded_df], ignore_index=True)
            st.success("Excel file appended successfully!")

        st.subheader("Add New Record (Optional)")
        with st.form("add_record_form"):
            server = st.text_input("Server")
            depot = st.text_input("Depot Name")
            fleet_number = st.text_input("Fleet Number")
            registration = st.text_input("Registration")
            issue = st.text_input("Issue")
            priority = st.selectbox("Priority", ["1", "2", "3"])
            comments = st.text_area("Comments")
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

            submitted = st.form_submit_button("Add Record")

            if submitted:
                new_row = {
                    "Server": server,
                    "Depot Name": depot,
                    "Fleet Number": fleet_number,
                    "Registration": registration,
                    "Issue": issue,
                    "Priority": priority,
                    "Comments": comments,
                    "Status": status,
                }
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Record added successfully!")

    # -------- VIEWER + ADMIN VIEW SECTION --------
    st.subheader("Records Table")
    columns_to_show = ["Depot Name", "Fleet Number", "Registration", "Priority"]
    st.dataframe(st.session_state.df[columns_to_show], use_container_width=True)

    st.subheader("Download Data")
    csv = st.session_state.df.to_csv(index=False)
    st.download_button("Download CSV", csv, "repair_dashboard.csv", "text/csv")
