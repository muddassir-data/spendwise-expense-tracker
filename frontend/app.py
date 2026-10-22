import os
import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_month import analytics_month_tab

ICON_PATH = os.path.join(os.path.dirname(__file__), "spendwise_icon.png")

st.set_page_config(page_title="SpendWise", page_icon="spendwise_icon.png")

col1, col2 = st.columns([1, 8])
with col1:
    st.image("spendwise_icon.png", width=60)
with col2:
    st.title("SpendWise")
st.subheader("Expense Tracking Platform")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Months"])

with tab1:
    add_update_tab()
with tab2:
    analytics_category_tab()
with tab3:
    analytics_month_tab()


