import pandas as pd
import sqlite3
import streamlit as st
import html


conn = sqlite3.connect('../../data/quotes.db')


df = pd.read_sql_query("SELECT * FROM mercado_livre_products", conn)

conn.close()

df['name'] = df['name'].fillna("Unknow").str.upper()

df.columns = df.columns.str.capitalize()

df.rename(columns={'_old_price': 'Old_Price', '_new_price': 'New_Price', '_source': 'Source'}, inplace=True)

st.title("Tênis Esportivos no Mercado Livre")
st.subheader('TABELA PRINCIPAL')
st.write(df)


# Usar a função st.markdown para criar um cabeçalho <h3> com HTML
st.markdown("<h4>Kpis de Novo Preço por Produto</h4>", unsafe_allow_html=True)
name_agg = df.groupby('Name')['New_Price'].agg(['min', 'max', 'mean', 'sum'])
st.write(name_agg)

col1, col2, col3 = st.columns(3)

total_itens = df.shape[0]
col1.metric(label="Numero Total de Items:", value=total_itens)

unique_brand = df['Name'].nunique()
col2.metric(label="Número Marcas Unicas", value=unique_brand)

avarage_new_price = df['New_Price'].mean()
col3.metric(label=" Preço Médio  novo", value=f"{avarage_new_price:.2f}")

