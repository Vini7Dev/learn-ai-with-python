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

csv_data

# st.write('Hello World!')
# st.write(csv_data[csv_data['Stream'] > 1000000000])

csv_data.set_index('Track', inplace=True)

# st.line_chart(csv_data[csv_data['Stream'] > 1000000000]['Stream'])

artists = csv_data['Artist'].value_counts().index
artist = st.selectbox("Artista", artists)
artist_results = csv_data[csv_data['Artist'] == artist]

albuns = artist_results['Album'].value_counts().index
algum = st.selectbox("Álbum", albuns)
album_results = csv_data[csv_data['Album'] == algum]

is_hide = st.checkbox('Esconder gráfico')

if not is_hide:
    st.bar_chart(album_results['Stream'])
