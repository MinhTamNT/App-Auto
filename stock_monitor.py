import requests
import pandas as pd
from datetime import datetime
from config import *

last_signals = {}

def send_notify_signal(symbol, signal_date, signal_type, current_price, recommended_price):
    payload = {
        'symbol': symbol,
        'type': signal_type,
        'date': signal_date,
        'price': current_price,
        'current_price': recommended_price
    }

    url = f"{API}?username={USERNAME}"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # print(f"Tín hiệu {signal_type} cho mã {symbol} đã được gửi thành công.")
            pass
        else:
            print(f"API thất bại với mã trạng thái: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")

def fetch_stock_data(symbol, start_date, end_date, resolution="1"):
    start = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    if symbol.startswith("VN30"):
        url = f"{API_GET_PRICE_VN30}?resolution={resolution}&ticker={symbol}&type=derivative&start={start}&to={end}&countBack=5"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data:
                prices = [{'time': row['tradingDate'], 'price': row['close']} for row in data['data']]
                return pd.DataFrame(prices)
            else:
                print("Không có dữ liệu từ VN30 API, thử API thay thế.")
        else:
            print(f"Lỗi từ VN30 API: {response.status_code}, {response.text}")

    url_alternative = f"{API_REAL_TIME}/v1/intraday/{symbol}/his/paging"
    response = requests.get(url_alternative)

    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data:
            prices = [{'time': row['t'], 'price': row['p']} for row in data['data']]
            return pd.DataFrame(prices)
        else:
            print("Không có dữ liệu từ API thay thế.")
    else:
        print(f"Lỗi từ API thay thế: {response.status_code}, {response.text}")

    return pd.DataFrame()

def calculate_ema(df, window=5):
    if len(df) < window:
        print(f"Not enough data to calculate EMA_{window}. Need at least {window} data points, but only have {len(df)}.")
        return df

    prices = df['price'].astype(float).values
    sma = sum(prices[:window]) / window
    alpha = 2 / (window + 1)
    ema_values = [sma]

    for price in prices[window:]:
        ema = (price - ema_values[-1]) * alpha + ema_values[-1]
        ema_values.append(ema)

    ema_series = [None] * (window - 1) + ema_values
    df[f'EMA_{window}'] = ema_series

    return df

def generate_signal(symbol, ema_df):
    current_price = ema_df.iloc[-1]['price']
    recommended_price = ema_df.iloc[-1]['EMA_5']
    signal_date = datetime.now().isoformat()
    if symbol not in last_signals:
        last_signals[symbol] = {'type': None, 'time': None}


    if current_price > recommended_price:
            send_notify_signal(symbol, signal_date, "1", current_price, current_price)
            return "Mua"
    elif current_price < recommended_price:
            send_notify_signal(symbol, signal_date, "2", current_price, current_price)
            return "Bán"

    print("Không có tín hiệu")
    return "Không có tín hiệu"

def convert_resolution_to_seconds(resolution):
    if resolution.isdigit():
        return int(resolution) * 60
    elif resolution == 'D':
        return 86400
    elif resolution == 'w':
        return 604800
    elif resolution == 'M':
        return 2592000
    else:
        raise ValueError("Invalid resolution format")
