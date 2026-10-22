import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_month_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")

    if response.status_code != 200:
        st.error("Failed to retrieve monthly analytics")
        return

    result = response.json()

    df = pd.DataFrame(result)

    st.title("Expense Breakdown By Months")
    st.bar_chart(data=df.set_index("month_name")["total"], use_container_width=True)

    df["total"] = df["total"].map("{:.2f}".format)
    df = df.rename(columns={"month_name": "Month Name", "total": "Total"})
    st.table(df[["Month Name", "Total"]])