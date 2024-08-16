import pandas as pd
import matplotlib.pyplot as plt

def backtest_with_drawdown_and_equity_curve(df, maxTrades = 5,initial_balance = 100000 ):
    balance = initial_balance  # Balance starts with initial balance
    net_profit = 0  # Initialize net profit to zero
    overall_profit = 0
    position = 0  # Position (positive for long, negative for short)
    total_positions = 0
    max_drawdown = 0
    max_profit = 0
    long_entry_price = []
    short_entry_price = []
    equity = initial_balance
    logs = []  # Store logs for debugging
    CycleProfit = []
    
    last_signal_index = -5  # Initialize to a value that allows the first signal to be processed
    
    # Lists to store balance and equity over time for plotting
    balance_over_time = []
    equity_over_time = []
    dates = []

    for i in reversed(df.index):
        close = df["close"][i]
        high = df["high"][i]
        low = df["low"][i]
        date = df['date'][i]
        log_entry = ""
        net_profit = 0  # Reset net profit for this iteration
        dd = 0
        
        # Calculate drawdown
        if len(short_entry_price) > 0:
            for x in range(len(short_entry_price)):  
                dd += short_entry_price[x] - high
                    
        
        if len(long_entry_price) > 0: 
            for x in range(len(long_entry_price)):     
                dd += low - long_entry_price[x] 
        
        equity = balance + dd
        if dd < max_drawdown:
            max_drawdown = dd
        if dd > max_profit:
            max_profit = dd
                
        # Save balance, equity, and dates for plotting
        balance_over_time.append(balance)
        equity_over_time.append(equity)
        dates.append(date)

        # Buy signal
        if df["signal"][i] == 1:
            if len(short_entry_price) > 0:  # Close all short positions
                for x in range(len(short_entry_price)):
                    profit =  short_entry_price[x] - close
                    log_entry = f"Closing short position, Profit: ${profit:.2f} position: {position}"
                    net_profit += profit
                    position += 1
                    logs.append(log_entry)
                log_entry = f"Net Profit: {net_profit}"
                balance += net_profit
                logs.append(log_entry)
                short_entry_price = []
                CycleProfit.append(net_profit)

            # Open long position
            if(len(long_entry_price) < maxTrades):
                if position == 0:
                    long_entry_price.append(close)  # Set entry price for long
                    position += 1
                    log_entry = f"Index: {i} | Date: {date} | Close: {close}, Opening long position at ${close:.2f} position: {position}"
                    logs.append(log_entry)
                    total_positions += 1
                elif position > 0:
                # Adjust position size if needed
                    long_entry_price.append(close) 
                    position += 1
                    log_entry = f"Index: {i} | Date: {date} | Close: {close}, Adding to long position at ${close:.2f} position: {position}"
                    logs.append(log_entry)
                    total_positions += 1
        
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
                balance += net_profit
                logs.append(log_entry)
                long_entry_price = []
                CycleProfit.append(net_profit)
            
            # Open short position
            if(len(short_entry_price) < maxTrades):
                if position == 0:
                    short_entry_price.append(close)
                    position -= 1
                    log_entry = f"Index: {i} | Date: {date} | Close: {close}, Opening short position at ${close:.2f} position: {position}"
                    logs.append(log_entry)
                    total_positions += 1
                elif position < 0 and len(long_entry_price) < maxTrades:
                # Adjust position size if needed
                    short_entry_price.append(close)
                    position -= 1
                    log_entry = f"Index: {i} | Date: {date} | Close: {close}, Adding to short position at ${close:.2f} position: {position}"
                    logs.append(log_entry)
                    total_positions += 1
    
    if len(short_entry_price) > 0:  # Close all short positions
        for x in range(len(short_entry_price)):
            profit =  short_entry_price[x] - close
            log_entry = f"Closing short position, Profit: ${profit:.2f} position: {position}"
            net_profit += profit
            position -= 1
            logs.append(log_entry)
        balance += net_profit
        CycleProfit.append(net_profit)
        short_entry_price = []

    if len(long_entry_price) > 0:  # Close all long positions
        for x in range(len(long_entry_price)):
            profit = close - long_entry_price[x]
            log_entry = f"Closing long position, Profit: ${profit:.2f} position: {position}"
            net_profit += profit
            position -= 1
            logs.append(log_entry) 
        balance += net_profit
        long_entry_price = []
        CycleProfit.append(net_profit)
    
    # Save logs for debugging
    logs_df = pd.DataFrame(logs, columns=['Log'])
    logs_df.to_csv('trading_logs.csv', index=False)
    
    # Print total net profit and loss
    print('Evaluation Metrics:')
    print('-----------------------------------')
    print(f"Start balance: ${initial_balance:.2f}")
    print(f"Closing Balance: ${(balance):.2f}")
    print(f"Total Positions: {total_positions:.2f}")
    print(f"Max MaxDrawdown: ${max_drawdown:.2f}")
    print(f"Max Profit Tardes: ${max_profit:.2f}")

    #for x in range(len(CycleProfit)):
        #print(f"{x} Profit: ${CycleProfit[x]:.2f}")


    # Plotting the balance and equity over time
    plt.figure(figsize=(14, 7))
    plt.plot(dates, balance_over_time, label='Balance', color='blue')
    plt.plot(dates, equity_over_time, label='Equity', color='green')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Balance and Equity over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
