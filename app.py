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

# show dataframe
col1, col2 = st.columns(2)
with col1:
    st.subheader("By Date, top...")
    st.write(sel_data)

# make key df
if sel_dtype in ('Keyword_single','Ticker_single'):
    cov_df = generic.single_key_df(sel_data, sel_key)
else:
    cov_df = generic.multi_key_df(sel_data)

# show dataframe 2 - single key
if sel_dtype in ('Keyword_single','Ticker_single'):
    with col2:
        st.subheader("By Key, top...")
        st.write(cov_df)

if st.button('Show Graph'):
    edge_list = graph.make_edge(cov_df)

    frontend.show_chart(graph.draw_graph(edge_list))