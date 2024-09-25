import requests
import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime

symbols = ["FPT", "VNM", "VCB"]

def fetch_stock_data(symbol):
    url = f"https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/{symbol}/his/paging"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        prices = [{'time': record['t'], 'price': record['p']} for record in data.get('data', [])]
        return prices
    else:
        print(f"Yêu cầu API cho {symbol} thất bại với mã trạng thái: {response.status_code}")
        return None

# Hàm tính EMA sử dụng pandas_ta
def calculate_ema(prices, window=20):
    df = pd.DataFrame(prices)
    df['price'] = df['price'].astype(float)
    df['EMA'] = ta.ema(df['price'], length=window)
    return df


def generate_signal(ema_df):
    if len(ema_df) < 2 or ema_df['EMA'].isnull().any():
        return None

    current_price = ema_df.iloc[-1]['price']
    previous_ema = ema_df.iloc[-2]['EMA']
    current_ema = ema_df.iloc[-1]['EMA']

    if current_price > current_ema and previous_ema >= current_ema:
        return "Tín hiệu mua"
    elif current_price < current_ema and previous_ema <= current_ema:
        return "Tín hiệu bán"
    else:
        return "Không có tín hiệu"


def run_stock_monitoring():
    while True:
        current_time = datetime.now().time()


        if current_time >= datetime.strptime('09:15', '%H:%M').time() and current_time <= datetime.strptime('17:00', '%H:%M').time():
            for symbol in symbols:
                prices = fetch_stock_data(symbol)

                if prices:
                    ema_df = calculate_ema(prices)
                    signal = generate_signal(ema_df)

                    print(f"Mã cổ phiếu: {symbol}")
                    print(f"Tín hiệu: {signal}")
                    print(f"Giá hiện tại: {ema_df.iloc[-1]['price']}, EMA: {ema_df.iloc[-1]['EMA']}")
                else:
                    print(f"Không lấy được dữ liệu cho mã {symbol}")


            print("\nChờ 1 phút...\n")
            time.sleep(60)
        else:
            print(f"Hiện tại ngoài giờ giao dịch (9:15 AM - 5:00 PM). Chờ đến giờ...\n")
            time.sleep(60)

run_stock_monitoring()
