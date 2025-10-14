import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = 'http://127.0.0.1:8000'

st.title('Расчет степени износа')

equipments = requests.get(f'{BASE_URL}/equipment/').json()
eq_options = {eq['name']: eq['id'] for eq in equipments}
selected_eq = st.selectbox('Оборудование', list(eq_options.keys()))
eq_id = eq_options.get(selected_eq)

zone_translation = {
    'Unknown': 'Неизвестно',
    'Green': 'Зелёный',
    'Yellow': 'Жёлтый',
    'Red': 'Красный',
    'Critical': 'Критический'
}

if eq_id:
    wear_data = requests.get(f'{BASE_URL}/wear/{eq_id}').json()
    df = pd.DataFrame(wear_data)
    df['zone'] = df['zone'].map(zone_translation)
    st.dataframe(df)

    fig = px.bar(df, x='part_name', y='remaining_percentage', color='zone',
                 color_discrete_map={
                     'Неизвестно': 'gray',
                     'Зелёный': 'green',
                     'Жёлтый': 'yellow',
                     'Красный': 'red',
                     'Критический': 'black'
                 },
                 title='Износ запчастей')
    st.plotly_chart(fig)