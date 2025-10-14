import streamlit as st
import requests
import pandas as pd

BASE_URL = 'http://127.0.0.1:8000'

st.title('Справочники')

tabs = st.tabs(['Оборудование', 'Запчасти', 'Мастерские', 'Типы замен'])

with tabs[0]:
    response = requests.get(f'{BASE_URL}/equipment/')
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
    with st.form('add_equipment'):
        name = st.text_input('Наименование')
        fleet_quantity = st.number_input('Количество в парке', min_value=1)
        if st.form_submit_button('Добавить'):
            requests.post(f'{BASE_URL}/equipment/', json={'name': name, 'fleet_quantity': fleet_quantity})
            st.rerun()

with tabs[1]:
    equipments = requests.get(f'{BASE_URL}/equipment/').json()
    eq_options = {eq['name']: eq['id'] for eq in equipments}
    response = requests.get(f'{BASE_URL}/parts/')
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
    with st.form('add_part'):
        name = st.text_input('Наименование')
        useful_life = st.number_input('Срок использования (дни)')
        equipment_name = st.selectbox('Оборудование', list(eq_options.keys()))
        quantity_per_equipment = st.number_input('Количество в оборудовании', min_value=1)
        stock_quantity = st.number_input('Количество на складе', min_value=0)
        procurement_time = st.number_input('Срок закупки (дни)')
        if st.form_submit_button('Добавить'):
            data = {
                'name': name, 'useful_life': useful_life, 'equipment_id': eq_options[equipment_name],
                'quantity_per_equipment': quantity_per_equipment, 'stock_quantity': stock_quantity,
                'procurement_time': procurement_time
            }
            requests.post(f'{BASE_URL}/parts/', json=data)
            st.rerun()

with tabs[2]:
    response = requests.get(f'{BASE_URL}/workshops/')
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
    with st.form('add_workshop'):
        name = st.text_input('Наименование')
        address = st.text_input('Адрес')
        if st.form_submit_button('Добавить'):
            requests.post(f'{BASE_URL}/workshops/', json={'name': name, 'address': address})
            st.rerun()

with tabs[3]:
    response = requests.get(f'{BASE_URL}/replacement_types/')
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
    with st.form('add_replacement_type'):
        name = st.text_input('Наименование')
        if st.form_submit_button('Добавить'):
            requests.post(f'{BASE_URL}/replacement_types/', json={'name': name})
            st.rerun()