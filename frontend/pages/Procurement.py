import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

BASE_URL = 'http://127.0.0.1:8000'

st.title('Формирование плана закупки')

parts = requests.get(f'{BASE_URL}/parts/').json()
part_options = {p['name']: p['id'] for p in parts}
selected_part = st.selectbox('Запчасть', list(part_options.keys()))
part_id = part_options.get(selected_part)
end_date = st.date_input('Дата окончания использования', value=date.today() + timedelta(days=365))

if part_id and end_date:
    proc_data = requests.get(f'{BASE_URL}/procurement/{part_id}?end_date={end_date}').json()
    st.write(f"Самая поздняя дата инициации: {proc_data['latest_init_date'] or 'Невозможно'}")

    all_proc = []
    for p in parts:
        resp = requests.get(f'{BASE_URL}/procurement/{p["id"]}?end_date={end_date}').json()
        all_proc.append(resp)
    df = pd.DataFrame(all_proc)
    st.dataframe(df)

    df['start'] = date.today()
    df['end'] = pd.to_datetime(df['latest_init_date'])
    fig = px.timeline(df, x_start='start', x_end='end', y='part_name', title='План инициаций')
    st.plotly_chart(fig)