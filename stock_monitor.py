import requests
import pandas as pd
from datetime import datetime
from config import *
import pandas_ta as ta


def send_notify_signal(symbol, signal_date, signal_type, price):
    payload = {
        'symbol': symbol,
        'type': signal_type,
        'date': signal_date,
        'price': price,
    }
    url = f"{API}?username?=minhtam1232"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Tín hiệu {signal_type} cho mã {symbol} đã được gửi thành công.")
        else:
            print(f"API thất bại với mã trạng thái: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")


def fetch_stock_data(symbol, start_date, end_date, resolution="1"):
    start = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    # Check if the symbol starts with "VN30"
    if symbol.startswith("VN30"):
        url = f"{API_GET_PRICE_VN30}?resolution={resolution}&ticker={symbol}&type=derivative&start={start}&to={end}&countBack=1"
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

    url_alternative = f"{API_REAL_TIME}{symbol}/his/paging"
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
    df['price'] = df['price'].astype(float)
    df['EMA_5'] = ta.ema(df['price'], length=window)

    return df


def generate_signal(symbol, ema_df):
    if len(ema_df) < 2 or ema_df['EMA_5'].isnull().any():
        return None

    price = ema_df.iloc[-1]['price']
    current_ema = ema_df.iloc[-1]['EMA_5']

    signal_date = datetime.now().isoformat()

    print(price > current_ema)

    print(price < current_ema)
    if price > current_ema:
        send_notify_signal(symbol, signal_date, "1", price)
        return "Tín hiệu mua"
    elif price < current_ema:
        send_notify_signal(symbol, signal_date, "2", price)
        return "Tín hiệu bán"
    else:
        return "Không có tín hiệu"
