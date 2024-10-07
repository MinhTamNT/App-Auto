import time
from datetime import datetime

import pandas as pd
from colorama import Fore

from stock_monitor import fetch_stock_data, calculate_ema, generate_signal


def run_stock_monitoring(symbols, start_date, end_date, resolution):
    dataframes = {symbol: pd.DataFrame(columns=['time', 'price']) for symbol in symbols}

    while True:
        current_time = datetime.now()

        start_trading_time = current_time.replace(hour=9, minute=15, second=0, microsecond=0).time()
        end_trading_time = current_time.replace(hour=15, minute=20, second=0, microsecond=0).time()

        if start_trading_time <= current_time.time() <= end_trading_time:
            for symbol in symbols:
                df = fetch_stock_data(symbol, start_date, end_date, resolution)

                if not df.empty:
                    if not dataframes[symbol].empty:
                        dataframes[symbol] = pd.concat([dataframes[symbol], df], ignore_index=True)
                    else:
                        dataframes[symbol] = df

                    if len(dataframes[symbol]) >= 5:
                        ema_df = calculate_ema(dataframes[symbol])
                        signal = generate_signal(symbol, ema_df , resolution)

                        current_price = ema_df.iloc[-1]['price']
                        ema_5 = ema_df.iloc[-1]['EMA_5']

                        formatted_current_price = f"{current_price:,.0f}".replace(',', '.').replace('.', ',', 1)
                        formatted_ema_5 = f"{ema_5:,.0f}".replace(',', '.').replace('.', ',', 1)

                        if signal == 'Mua':
                            signal_color = Fore.GREEN
                        elif signal == 'Bán':
                            signal_color = Fore.RED
                        else:
                            signal_color = Fore.WHITE

                        print(f"Mã CK:  {symbol}")
                        print(f"Tín hiệu: {signal_color}{signal}{Fore.RESET}")
                        print(f"Giá hiện tại: {formatted_current_price}")
                        print(f"EMA_5: {formatted_ema_5}")
                        print("===========================================================\n")

                    else:
                        print(f"Không đủ dữ liệu cho {symbol} để tính toán EMA. Cần 5 điểm dữ liệu, hiện có {len(dataframes[symbol])}.")
                else:
                    print(f"Không lấy được dữ liệu cho mã {symbol}")

            if resolution.isdigit():
                minutes = int(resolution)
                print(f"\nChờ {minutes} phút...\n")
                time.sleep(minutes * 60)
            elif resolution.upper() == "D":
                print("\nChờ 1 ngày...\n")
                time.sleep(24 * 60 * 60)
            elif resolution.upper() == "M":
                print("\nChờ 1 tháng...\n")
                time.sleep(30 * 24 * 60 * 60)
            else:
                print("\nĐộ phân giải không hợp lệ.\n")
                break

        else:
            print(f"Hiện tại là {current_time.strftime('%H:%M:%S')}, ngoài giờ giao dịch (9:15 AM - 3:00 PM). Chờ đến giờ...\n")
            time.sleep(60)

if __name__ == "__main__":
    """
     Tham số của resolution :
        - 1 : 1 phút
        - 5 : 5 phút
        - 15 : 15 phút
        - 60 : 1 gi
        - D : 1 ngày
        - M : 1 Tháng
        - w : 1 ngày
    - lưu ý tham số của resolution theo tiêu chuẩn định nghĩa sẵn của API của TBCS nên dùng những tham số trên nhá.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    start_date = current_date

    end_date = current_date

    symbols = ["FPT"]

    # Can be "1", "5", "15", "60", "D", or "M"
    resolution = "1"

    run_stock_monitoring(symbols, start_date, end_date, resolution)
