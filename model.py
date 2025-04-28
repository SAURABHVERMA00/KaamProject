import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load your dataset
df = pd.read_excel('/content/drive/MyDrive/large_solar_power_data.xlsx')  # <-- Make sure the file is in your working directory

# Preprocessing
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
df['HOUR'] = df['DATE_TIME'].dt.hour
df['DAY'] = df['DATE_TIME'].dt.day
df['MONTH'] = df['DATE_TIME'].dt.month
df['YEAR'] = df['DATE_TIME'].dt.year

# Features and target
features = ['DC_POWER', 'AC_POWER', 'EXPORTED_POWER', 'HOUR', 'DAY', 'MONTH', 'YEAR']
target = 'LOAD_CONSUMPTION'

X = df[features]
y = df[target]

# Train-test split
split_index = int(0.8 * len(df))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Train Random Forest Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Future 1-Day Prediction
last_date = df['DATE_TIME'].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(minutes=15), periods=96, freq='15T')

# Create future features
future_features = pd.DataFrame({
    'HOUR': future_dates.hour,
    'DAY': future_dates.day,
    'MONTH': future_dates.month,
    'YEAR': future_dates.year
})

# Fill unknown DC_POWER, AC_POWER, EXPORTED_POWER with training means
future_features['DC_POWER'] = X_train['DC_POWER'].mean()
future_features['AC_POWER'] = X_train['AC_POWER'].mean()
future_features['EXPORTED_POWER'] = X_train['EXPORTED_POWER'].mean()

# Reorder columns
future_features = future_features[['DC_POWER', 'AC_POWER', 'EXPORTED_POWER', 'HOUR', 'DAY', 'MONTH', 'YEAR']]

# Predict future load
future_predictions = rf_model.predict(future_features)

# Save predictions
future_df = pd.DataFrame({
    'Timestamp': future_dates,
    'Predicted_Load_kW': future_predictions
})

# Save predictions to Excel
future_df.to_excel('future_load_predictions.xlsx', index=False)
print("Predictions saved to 'future_load_predictions.xlsx' ✅")

# Plot predictions
plt.figure(figsize=(12,6))
plt.plot(future_dates, future_predictions, marker='o', linestyle='-', color='green')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.xticks(rotation=45)
plt.xlabel('Timestamp')
plt.ylabel('Predicted Load Consumption (kW)')
plt.title('Predicted Load Consumption for Next 1 Day (Hourly)')
plt.grid(True)
plt.tight_layout()

# Save plot as PNG
plt.savefig('future_load_plot.png')
plt.show()
print("Prediction graph saved as 'future_load_plot.png' 📈")