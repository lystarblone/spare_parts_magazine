import streamlit as st
import requests
import pandas as pd

BASE_URL = 'http://127.0.0.1:8000'

st.title('Случаи замен запчастей')

equipments = requests.get(f'{BASE_URL}/equipment/').json()
eq_options = {eq['name']: eq['id'] for eq in equipments}
selected_eq = st.selectbox('Выберите оборудование', list(eq_options.keys()))
eq_id = eq_options.get(selected_eq)

if eq_id:
    replacements = requests.get(f'{BASE_URL}/replacements/?equipment_id={eq_id}').json()
    df = pd.DataFrame(replacements)
    edited_df = st.data_editor(df, num_rows='dynamic')

    if st.button('Сохранить изменения'):
        for idx, row in edited_df.iterrows():
            requests.put(f'{BASE_URL}/replacements/{row['id']}', json=row.to_dict())
        st.success('Сохранено')

    with st.form('add_replacement'):
        parts = requests.get(f'{BASE_URL}/parts/').json()
        part_options = {p['name']: p['id'] for p in parts if p['equipment_id'] == eq_id}
        part_id = st.selectbox('Запчасть', list(part_options.keys()))
        replacement_date = st.date_input('Дата замены')
        types = requests.get(f'{BASE_URL}/replacement_types/').json()
        type_options = {t['name']: t['id'] for t in types}
        type_id = st.selectbox('Тип замены', list(type_options.keys()))
        workshops = requests.get(f'{BASE_URL}/workshops/').json()
        ws_options = {w['name']: w['id'] for w in workshops}
        ws_id = st.selectbox('Мастерская', list(ws_options.keys()))
        if st.form_submit_button('Добавить'):
            data = {
                'equipment_id': eq_id, 'part_id': part_options[part_id],
                'replacement_date': str(replacement_date), 'replacement_type_id': type_options[type_id],
                'workshop_id': ws_options[ws_id]
            }
            requests.post(f'{BASE_URL}/replacements/', json=data)
            st.rerun()