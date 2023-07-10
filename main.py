import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

#Title
st.title('Stock History App')

st.sidebar.title('Selecione a ação')
ticker_symbol_1 = st.sidebar.text_input('stock', 'ITSA4.SA', max_chars=10)
ticker_symbol_2 = st.sidebar.text_input('stock', 'BBAS3.SA', max_chars=10)

data_T1 = yf.download(ticker_symbol_1, start='2020-01-01', end='2023-06-26')
data_T2 = yf.download(ticker_symbol_2, start='2020-01-01', end='2023-06-26')

st.subheader('History')
st.dataframe(data_T1)
st.dataframe(data_T2)

fig = make_subplots(rows=2, cols=1)
fig.append_trace(go.Scatter(x=data_T1.index, y=data_T1['Close'], name=f'{ticker_symbol_1}'), row=1, col=1)
fig.append_trace(go.Scatter(x=data_T2.index, y=data_T2['Close'], name=f'{ticker_symbol_2}'), row=2, col=1)
fig.update_layout(title='Comparação', xaxis_title='Date', yaxis_title='Preço')
st.plotly_chart(fig)
