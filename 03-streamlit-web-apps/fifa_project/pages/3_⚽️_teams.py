import streamlit as st

st.set_page_config(
    page_title='Teams',
    page_icon='⚽️',
    layout='wide',
)

df_data = st.session_state['data']

teams = df_data['Club'].value_counts().index
team = st.sidebar.selectbox('Time', teams)

df_players = df_data[df_data['Club'] == team].set_index('Name')

st.image(df_players.iloc[0]['Club Logo'])

st.markdown(f"## {team}")

columns_to_show = ['Age', 'Photo', 'Flag', 'Overall', 'Value(£)', 'Wage(£)', 'Joined',
           'Height(cm.)', 'Weight(lbs.)', 'Contract Valid Until', 'Release Clause(£)']

st.dataframe(
    df_players[columns_to_show],
    column_config={
        'Overall': st.column_config.ProgressColumn(
            'Overall', format='%d', min_value=0, max_value=100,
        ),
        'Wage(£)': st.column_config.ProgressColumn(
            'Weekly Wage', format='£%f', min_value=0, max_value=df_players['Wage(£)'].max(),
        ),
        'Photo': st.column_config.ImageColumn(),
        'Flag': st.column_config.ImageColumn('Country'),
    },
)
