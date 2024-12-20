import streamlit as st
import pandas as pd
import time

# STREAMLIT DOCS: https://docs.streamlit.io/
# EXECUTE: python -m streamlit run .\__init__.py

csv_data = pd.read_csv('data/01 Spotify.csv')

csv_data

# st.write(csv_data[csv_data['Stream'] > 1000000000])

csv_data.set_index('Artist', inplace=True)

st.line_chart(csv_data[csv_data['Stream'] > 1000000000]['Stream'])
