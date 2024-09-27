import pandas as pd
from stock_monitor import fetch_stock_data, calculate_ema, generate_signal
import time
from datetime import datetime


def run_stock_monitoring(symbols, start_date, end_date, resolution):
    dataframes = {symbol: pd.DataFrame(columns=['time', 'price']) for symbol in symbols}

    while True:
        current_time = datetime.now()


        start_trading_time = current_time.replace(hour=9, minute=15, second=0, microsecond=0).time()
        end_trading_time = current_time.replace(hour=15, minute=0, second=0, microsecond=0).time()


        if start_trading_time <= current_time.time() <= end_trading_time:
            for symbol in symbols:
                df = fetch_stock_data(symbol, start_date, end_date, resolution)

                if not df.empty:
                    if not dataframes[symbol].empty:
                        dataframes[symbol] = pd.concat([dataframes[symbol], df], ignore_index=True)
                    else:
                        dataframes[symbol] = df

                    ema_df = calculate_ema(dataframes[symbol])

                    signal = generate_signal(symbol, ema_df)

                    print(f"Mã cổ phiếu: {symbol}")
                    print(f"Tín hiệu: {signal}")
                    print(f"Giá hiện tại: {ema_df.iloc[-1]['price']}, EMA_5: {ema_df.iloc[-1]['EMA_5']}")
                else:
                    print(f"Không lấy được dữ liệu cho mã {symbol}")

            print(f"\nChờ {resolution}...\n")
            time.sleep(60)
        else:
            print(f"Hiện tại là {current_time.strftime('%H:%M:%S')}, ngoài giờ giao dịch (9:15 AM - 3:00 PM). Chờ đến giờ...\n")
            time.sleep(60)


if __name__ == "__main__":
    start_date = "2024-09-27"
    end_date = "2024-09-27"
    symbols = ["VN30F2410", "FPT"]
    resolution = "1"
    run_stock_monitoring(symbols, start_date, end_date, resolution)
