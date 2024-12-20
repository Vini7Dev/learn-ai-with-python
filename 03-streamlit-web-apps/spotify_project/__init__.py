import streamlit as st
import pandas as pd
import time

# STREAMLIT DOCS: https://docs.streamlit.io/
# EXECUTE: python -m streamlit run .\__init__.py

st.set_page_config(
    layout='wide',
    page_title='spotify songs',
)

csv_data = pd.read_csv('data/01 Spotify.csv')

# st.write('Hello World!')
# st.write(csv_data[csv_data['Stream'] > 1000000000])

csv_data.set_index('Track', inplace=True)

# st.line_chart(csv_data[csv_data['Stream'] > 1000000000]['Stream'])

artists = csv_data['Artist'].value_counts().index
artist = st.sidebar.selectbox("Artista", artists)
artist_results = csv_data[csv_data['Artist'] == artist]

albuns = artist_results['Album'].value_counts().index
algum = st.sidebar.selectbox("Álbum", albuns)
album_results = csv_data[csv_data['Album'] == algum]

is_hide = st.checkbox('Esconder gráfico')

if not is_hide:
    col1, col2 = st.columns([0.7, 0.3])

    col1.bar_chart(album_results['Stream'])

    col2.line_chart(album_results['Danceability'])

csv_data
