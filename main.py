import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

#Title
st.title('Stock History App')

st.sidebar.title('Selecione a ação')
ticker_symbol = st.sidebar.text_input('stock', 'AAPL', max_chars=10)

data = yf.download(ticker_symbol, start='2020-01-01', end='2023-06-26')

st.subheader('History')
st.dataframe(data)

fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Fechamento'))
fig.update_layout(title=f'{ticker_symbol}', xaxis_title='Date', yaxis_title='Preço')
st.plotly_chart(fig)
