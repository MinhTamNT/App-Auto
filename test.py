import pandas as pd

# Example function to calculate EMA
def calculate_ema(data, span=5):
    df = pd.DataFrame(data)
    df['EMA_5'] = df['close'].ewm(span=span, adjust=False).mean()
    return df

# Example function to generate buy signal based on EMA and current price
def generate_signal(df):
    # The signal could be 'Buy' if the current price is lower than EMA
    current_price = df.iloc[-1]['close']
    ema_5 = df.iloc[-1]['EMA_5']

    if current_price < ema_5:
        return "Buy", ema_5, current_price
    else:
        return "Hold", ema_5, current_price

# Example stock data
data = [
    {"open": 1344, "high": 1344, "low": 1344, "close": 1344, "volume": 5589, "tradingDate": "2024-09-25T07:45:00.000Z"},
    {"open": 1350, "high": 1355, "low": 1348, "close": 1350, "volume": 6100, "tradingDate": "2024-09-24T07:45:00.000Z"},
    {"open": 1338, "high": 1340, "low": 1335, "close": 1339, "volume": 5734, "tradingDate": "2024-09-23T07:45:00.000Z"},
    {"open": 1327, "high": 1333, "low": 1325, "close": 1329, "volume": 5400, "tradingDate": "2024-09-22T07:45:00.000Z"},
    {"open": 1312, "high": 1320, "low": 1310, "close": 1315, "volume": 5100, "tradingDate": "2024-09-21T07:45:00.000Z"},
    {"open": 1295, "high": 1305, "low": 1290, "close": 1300, "volume": 4800, "tradingDate": "2024-09-20T07:45:00.000Z"},
    {"open": 1280, "high": 1290, "low": 1275, "close": 1285, "volume": 4500, "tradingDate": "2024-09-19T07:45:00.000Z"},
    {"open": 1265, "high": 1275, "low": 1260, "close": 1270, "volume": 4200, "tradingDate": "2024-09-18T07:45:00.000Z"},
    {"open": 1250, "high": 1260, "low": 1245, "close": 1255, "volume": 4000, "tradingDate": "2024-09-17T07:45:00.000Z"},
    {"open": 1235, "high": 1245, "low": 1230, "close": 1240, "volume": 3900, "tradingDate": "2024-09-16T07:45:00.000Z"}
]


# Calculate EMA and generate signal
df = calculate_ema(data)
signal, recommended_price, current_price = generate_signal(df)

# Output the results
print(f"Signal: {signal}")
print(f"Recommended Price (EMA): {recommended_price}")
print(f"Current Price: {current_price}")
