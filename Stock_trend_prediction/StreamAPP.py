import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import yfinance as yf

start = '2010-01-01'
end = '2023-09-20'

# st.title('Stock Trend Prediction')
# yf ='yahoo'
# user_input = st.text_input('Enter Stock Ticker', 'AAPL')
# df =data.DataReader(user_input,'yahoo',start,end)

# st.subheader('Data from 2010 -2023')
# st.write(df.desrcibe())

st.title("Stock Trend Prediction")

# User input for stock symbol and date range
user_input = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start = st.date_input("Select Start Date:")
end = st.date_input("Select End Date:")

# Fetch stock data using yfinance
df = yf.download(user_input, start=start, end=end)

# Display the dataframe
st.dataframe(df)

# --------
# Visualizations
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'g')
plt.plot(ma200, 'o')
plt.plot(df.Close, 'b')
st.pyplot(fig)

# Splitting data into Training
data_training = pd.DataFrame(df['Close'][0:int(len(df) * 0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df) * 0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(data_training)

# Model loading
model = load_model('keras_model.h5')

# Testing
past_100_days = data_training.tail(100)

final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Final graph
st.subheader('Prediction vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'y', label='Original Price')
plt.plot(y_predicted, 'g', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()  # Display the plot
st.pyplot(fig2)
