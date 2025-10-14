import streamlit as st

st.set_page_config(page_title='Журнал запасных частей', layout='wide')

st.sidebar.title('Навигация')
st.sidebar.markdown('''
- [Справочники](/Directories)
- [Замены](/Replacements)
- [Износ](/Wear)
- [План закупок](/Procurement)
''')

st.title('Журнал запасных частей')
st.write('Используйте боковое меню для навигации. Данные взаимодействуют с локальной БД через API.')