import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta, datetime

np.random.seed(42)

n_days = 365  # Simulate a year's worth of data
dates = pd.date_range(start="2023-01-01", periods=n_days, freq="D")
data = 10 + 5 * np.sin(np.linspace(0, 3 * np.pi, n_days)) + np.random.normal(0, 0.5, n_days)

# Create DataFrame
time_series_data = pd.DataFrame({"Date": dates, "Temperature": data})
# Split data into training and testing sets
train_size = int(len(time_series_data) * 0.8)  
train_data = time_series_data["Temperature"][:train_size]
test_data = time_series_data["Temperature"][train_size:]


model_order = (5, 1, 0)  # ARIMA(p, d, q) model parameters
model = ARIMA(train_data, order=model_order)
model_fit = model.fit()


forecast_days = len(test_data)
forecast = model_fit.forecast(steps=forecast_days)


plt.figure(figsize=(15, 7))
plt.plot(time_series_data["Date"], time_series_data["Temperature"], label="Actual Temperature")
plt.plot(time_series_data["Date"].iloc[train_size:], forecast, color='red', linestyle='--', label="Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Time-Series Forecast Visualization using ARIMA")
plt.legend()
plt.show()
