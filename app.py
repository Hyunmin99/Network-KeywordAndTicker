import streamlit as st
import generic
import frontend
import graph

################################################
# Header and preprocessing

# set page layout
st.set_page_config(layout="wide")

# Set Title
st.title('Network Graph for Keyword and Ticker')

################################################
# Sidebar section
sel_dtype, sel_date, sel_head, sel_key, sel_data = frontend.display_sidebar()

################################################
# Main section

st.dataframe(sel_data)

# make key df
if sel_dtype in ('Keyword_single','Ticker_single'):
    cov_df = generic.single_key_df(sel_data, sel_key)
else:
    cov_df = generic.multi_key_df(sel_data)
    
st.dataframe(cov_df)

frontend.show_chart(cov_df)