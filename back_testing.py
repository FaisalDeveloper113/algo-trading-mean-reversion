import pandas as pd

def backtest_with_drawdown_and_equity_curve(df):
    initial_balance = 0  # Starting balance
    balance = initial_balance  # Balance starts with initial balance
    net_profit = 0  # Initialize net profit to zero
    overall_profit = 0
    position = 0  # Position (positive for long, negative for short)
    total_positions = 0;
    long_entry_price = []
    short_entry_price = []

    
    logs = []  # Store logs for debugging
    
    last_signal_index = -5  # Initialize to a value that allows the first signal to be processed
    
    for i in reversed(df.index):
        close = df["close"][i]
        date = df['date'][i]
        log_entry = ""
        # Reset net profit for this iteration
        net_profit = 0

        # Buy signal
        if df["signal"][i] == 1:
            if len(short_entry_price) > 0:  # Close all short positions
                for x in range(len(short_entry_price)):
                    profit =  short_entry_price[x] - close
                    log_entry = f"Closing short position, Profit: ${profit:.2f} position: {position}"
                    net_profit += profit
                    position -= 1
                    logs.append(log_entry)
                log_entry = f"Net Profit: {net_profit}"
                overall_profit+=net_profit
                logs.append(log_entry)
                short_entry_price = []

            # Open long position
            if position == 0:
                long_entry_price.append(close)  # Set entry price for long
                position += 1
                log_entry = f"Index: {i} | Date: {date} | Close: {close}, Opening long position at ${close:.2f} position: {position}"
                logs.append(log_entry)
                total_positions+=1
            elif position > 0:
                # Adjust position size if needed
                long_entry_price.append(close) 
                position += 1
                log_entry = f"Index: {i} | Date: {date} | Close: {close}, Adding to long position at ${close:.2f} position: {position}"
                logs.append(log_entry)
                total_positions+=1
        
        # Sell signal
        elif df["signal"][i] == -1:
            if len(long_entry_price) > 0:  # Close all long positions
                for x in range(len(long_entry_price)):
                    profit = close - long_entry_price[x]
                    log_entry = f"Closing long position, Profit: ${profit:.2f} position: {position}"
                    net_profit += profit
                    position -= 1
                    logs.append(log_entry)
                log_entry = f"Net Profit<><><><><><><><: {net_profit}"
                overall_profit+=net_profit
                logs.append(log_entry)
                long_entry_price = []
            # Open short position
            if position == 0:
                short_entry_price.append(close)
                position -= 1
                log_entry = f"Index: {i} | Date: {date} | Close: {close}, Opening short position at ${close:.2f} position: {position}"
                logs.append(log_entry)
                total_positions+=1
            elif position < 0:
                # Adjust position size if needed
                short_entry_price.append(close)
                position -= 1
                log_entry = f"Index: {i} | Date: {date} | Close: {close}, Adding to short position at ${close:.2f} position: {position}"
                logs.append(log_entry)
                total_positions+=1
        
    
    if len(short_entry_price) > 0:  # Close all short positions
        for x in range(len(short_entry_price)):
            profit =  short_entry_price[x] - close
            log_entry = f"Closing short position, Profit: ${profit:.2f} position: {position}"
            net_profit += profit
            position -= 1
            logs.append(log_entry)
            overall_profit+=net_profit
        short_entry_price = []
    if len(long_entry_price) > 0:  # Close all long positions
        for x in range(len(long_entry_price)):
            profit = close - long_entry_price[x]
            log_entry = f"Closing long position, Profit: ${profit:.2f} position: {position}"
            net_profit += profit
            position -= 1
            logs.append(log_entry)
            overall_profit+=net_profit    
        long_entry_price = []
    
    
    # Save logs for debugging
    logs_df = pd.DataFrame(logs, columns=['Log'])
    logs_df.to_csv('trading_logs.csv', index=False)
    
    
    # Print total net profit and loss
    print('Evaluation Metrics:')
    print('-----------------------------------')
    total_net_profit = balance - initial_balance
    print(f"Start balance: ${balance:.2f}")
    print(f"OverAll Profit: ${overall_profit:.2f}")
    print(f"Closing Balance: ${(balance+overall_profit):.2f}")
    print(f"Total Positions: ${total_positions:.2f}")

    print()

