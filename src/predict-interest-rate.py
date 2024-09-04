import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('brazilian-interest-rates-history.csv')

# Convert Date to datetime and sort by date
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values(by='Date')

# Create a new feature for the previous month's interest rate
# This will serve as our feature to predict the next month
df['PreviousMonthRate'] = df['Value'].shift(1)

# Drop any missing values created by the shift operation
df = df.dropna()

# Prepare the features (X) and labels (y)
X = df[['PreviousMonthRate']]  # Feature is the previous month's rate
y = df['Value']  # Label is the current month's rate

# Split the data into training and test sets
# We'll use 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the interest rate for the next month
y_pred = model.predict(X_test)

# Visualize the results in a chart
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.title('Interest Rate Prediction')
plt.xlabel('Previous Month Rate')
plt.ylabel('Interest Rate')
plt.legend()
plt.show()

# Model performance
# Calculate the R-squared value to measure the model's performance (values close to 1 mean a better fit)
r_squared = model.score(X_test, y_test)
print(f'R-squared: {r_squared:.2f}')

# You can also predict for the next month by taking the last rate in your data:
last_month_rate = df['Value'].iloc[-1]
predicted_next_month_rate = model.predict(np.array([[last_month_rate]]))
print(f"Predicted Interest Rate for Next Month: {predicted_next_month_rate[0]:.2f}")