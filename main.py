import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas
import numpy as np

start = '2020-01-01'
end = '2023-07-15'

#Title
st.title('Stock History App')

#SIDEBAR
st.sidebar.title('Selecione a ação')
ticker_symbol_1 = st.sidebar.text_input('Ticker', 'ITSA4.SA', max_chars=10)
st.sidebar.title('Detalhes do RSI')
periods_rsi = st.sidebar.text_input('Período', '14', max_chars=2)
st.sidebar.title('Detalhes do EMA')
periods_ema = st.sidebar.text_input('Período', '10', max_chars=3)
smoothing_ema = st.sidebar.text_input('Suavização', '2', max_chars=3)

#DOWNLOAD DATA
data_T1 = yf.download(ticker_symbol_1, start=start, end=end)

#EMA
ema = [sum(data_T1['Close'][:int(periods_ema)])/int(periods_ema)]
for price in data_T1['Close'][int(periods_ema):]:
    ema.append((price * (int(smoothing_ema) / (1 + int(periods_ema)))) + ema[-1] * (1 - (int(smoothing_ema) / (1 + int(periods_ema)))))

price_X = np.arange(data_T1.shape[0])
ema_X = np.arange(int(smoothing_ema), data_T1.shape[0]+1)

#SUBHEADER
st.subheader('History')

#HISTORY
st.dataframe(data_T1)

#RSI
close_delta = data_T1['Close'].diff()

up = close_delta.clip(lower=0)
down = -1 * close_delta.clip(upper=0)

ma_up = up.rolling(window = int(periods_rsi)).mean()
ma_down = down.rolling(window=int(periods_rsi)).mean()

rsi = ma_up / ma_down
rsi = 100 - (100/(1+rsi))

#PLOT
fig = make_subplots(rows=3, cols=1)
fig.append_trace(go.Scatter(x=data_T1.index, y=data_T1['Close'], name=f'{ticker_symbol_1}'), row=1, col=1)
fig.append_trace(go.Scatter(x=ema_X, y=ema, name='EMA'), row=2, col=1)
fig.append_trace(go.Scatter(x=data_T1.index, y=rsi, name='RSI'), row=3, col=1)
fig.update_layout(title=f'Gráficos para {ticker_symbol_1}', xaxis_title='Date', yaxis_title='Preço')
st.plotly_chart(fig)
