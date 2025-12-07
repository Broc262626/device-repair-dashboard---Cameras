
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cameras & Tasks Repair Dashboard", page_icon="assets/logo.png")

st.image("assets/logo.png", width=120)
st.title("Cameras & Tasks Repair Dashboard")

# Load data
df_path = "data/devices.csv"
try:
    df = pd.read_csv(df_path)
except:
    df = pd.DataFrame(columns=["id","device_name","device_type","location","status","last_inspection","notes","assignee"])

# Import section
st.subheader("Import Excel/CSV")
uploaded = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"])
if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
    df.to_csv(df_path, index=False)
    st.success("Imported successfully!")

# Show table
st.subheader("Current Records")
st.dataframe(df)

# Export
st.download_button("Export CSV", df.to_csv(index=False), "devices_export.csv")
