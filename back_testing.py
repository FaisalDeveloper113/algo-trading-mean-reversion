import pandas as pd

def backtest_dataframe(df):
    position = 0  # Current position in lots (positive for long, negative for short)
    net_profit = 0
    df['buy_date'] = ''
    df['sell_date'] = ''
    df['short_open_date'] = ''
    df['short_close_date'] = ''
    
    buy_prices = []
    buy_positions = []
    short_prices = []
    short_positions = []
    total_gains = 0
    total_losses = 0
    logs = []  # List to store log entries

    for i in reversed(df.index):
        close = df["close"][i]
        date = df['date'][i]
        log_entry = f"Index: {i} | Date: {date}"  # Reset log_entry for each iteration

        # Buy action
        if df["signal"][i] == 1:
            if position < 0:  # Close all short positions if any
                for j in range(len(short_prices)):
                    short_profit = short_prices[j] - close
                    profit_or_loss = short_profit * abs(short_positions[j])
                    if profit_or_loss > 0:
                        total_gains += profit_or_loss
                        log_entry += f", Profit for short trade {j+1}: ${profit_or_loss:.2f}"
                    else:
                        total_losses += abs(profit_or_loss)
                        log_entry += f", Loss for short trade {j+1}: ${abs(profit_or_loss):.2f}"
                    net_profit += profit_or_loss

                df.at[i, 'short_close_date'] = date
                log_entry += f", Closing Short Position at {close}, Net Profit: ${net_profit:.2f}"
                logs.append(log_entry)  # Add log entry
                short_prices = []
                short_positions = []
                position = 0

            if position > 0:  # Add to existing long position
                buy_prices.append(close)
                buy_positions.append(1)
                df.at[i, 'buy_date'] = date
                log_entry += f", Adding to Long Position at {close}, Buy Open Price: {buy_prices[0]}"
                logs.append(log_entry)  # Add log entry
                position += 1
                
            elif position == 0:  # Start a new long position
                buy_prices.append(close)
                buy_positions.append(1)
                df.at[i, 'buy_date'] = date
                log_entry += f", Opening Long Position at {close}, Buy Open Price: {close}"
                logs.append(log_entry)  # Add log entry
                position += 1

        # Sell action
        elif df["signal"][i] == -1:
            if position > 0:  # Close all long positions
                for j in range(len(buy_prices)):
                    buy_profit = close - buy_prices[j]
                    profit_or_loss = buy_profit * buy_positions[j]
                    if profit_or_loss > 0:
                        total_gains += profit_or_loss
                        log_entry += f", Profit for long trade {j+1}: ${profit_or_loss:.2f}"
                    else:
                        total_losses += abs(profit_or_loss)
                        log_entry += f", Loss for long trade {j+1}: ${abs(profit_or_loss):.2f}"
                    net_profit += profit_or_loss

                df.at[i, 'sell_date'] = date
                log_entry += f", Closing Long Position at {close}, Net Profit: ${net_profit:.2f}"
                logs.append(log_entry)  # Add log entry
                buy_prices = []
                buy_positions = []
                position = 0

            if position == 0:  # Open a new short position
                short_prices.append(close)
                short_positions.append(-1)
                df.at[i, 'short_open_date'] = date
                log_entry += f", Opening Short Position at {close}, Short Open Price: {close}"
                logs.append(log_entry)  # Add log entry
                position -= 1

            elif position < 0:  # Increase short position size
                short_prices.append(close)
                short_positions.append(-1)
                df.at[i, 'short_open_date'] = date
                log_entry += f", Adding to Short Position at {close}, Short Open Price: {short_prices[0]}"
                logs.append(log_entry)  # Add log entry
                position -= 1

    # Save all logs to a CSV file
    logs_df = pd.DataFrame(logs, columns=['Log'])
    logs_df.to_csv('trading_logs.csv', index=False)
    
    # Save results to a CSV file
    results = {
        'Total Net Profit': [net_profit],
        'Total Gains': [total_gains],
        'Total Losses': [total_losses]
    }
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('trading_results.csv', index=False)
    
    # Print total net profit and loss
    print()
    print('Evaluation Metrics:')
    print('-----------------------------------')
    print(f"Total Net Profit: ${net_profit:.2f}")
    print(f"Total Gains: ${total_gains:.2f}")
    print(f"Total Losses: ${total_losses:.2f}")
    print()

