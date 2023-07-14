import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas

start = '2020-01-01'
end = '2023-07-14'

#Title
st.title('Stock History App')

st.sidebar.title('Selecione a ação')
ticker_symbol_1 = st.sidebar.text_input('Stock', 'ITSA4.SA', max_chars=10)
st.sidebar.title('Período para RSI')
periods = st.sidebar.text_input('RSI', '14', max_chars=2)

data_T1 = yf.download(ticker_symbol_1, start=start, end=end)

st.subheader('History')
st.dataframe(data_T1)

close_delta = data_T1['Close'].diff()

up = close_delta.clip(lower=0)
down = -1 * close_delta.clip(upper=0)

ma_up = up.rolling(window = int(periods)).mean()
ma_down = down.rolling(window=int(periods)).mean()

rsi = ma_up / ma_down
rsi = 100 - (100/(1+rsi))

fig = make_subplots(rows=2, cols=1)
fig.append_trace(go.Scatter(x=data_T1.index, y=data_T1['Close'], name=f'{ticker_symbol_1}'), row=1, col=1)
fig.append_trace(go.Scatter(x=data_T1.index, y=rsi, name='RSI'), row=2, col=1)
fig.update_layout(title=f'Gráficos para {ticker_symbol_1}', xaxis_title='Date', yaxis_title='Preço')
st.plotly_chart(fig)
