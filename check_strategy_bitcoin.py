import pandas as pd


def load_price_data(csv_file_path):

    df = pd.read_csv(csv_file_path)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')  # Convert to IST


    return df



def calculate_score(csv_file, date_str):
        # Load Bitcoin price data (assuming it has columns: time, open, high, low, close)
    bitcoin_data = load_price_data('./csv_data/bitcoin_price_data.csv')

    # Load event data (assuming it has columns: start_time, end_time, target_price, settled_as)

    bitcoin_data = bitcoin_data.sort_values(by='time')
    bitcoin_data.set_index('time', inplace=True)
    # print(bitcoin_data.head())

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert the 'start_time' column to datetime
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # Filter data based on the input date
    date = pd.to_datetime(date_str)
    df = df[df['end_time'].dt.date == date.date()]

    # Sort by start_time to ensure the data is in chronological order
    df = df.sort_values(by='start_time').reset_index(drop=True)

    # Initialize the score
    score = 0
    max_profit = 0
    max_loss = 0
    # Apply the strategy
    previous_value = None
    consecutive_count = 0

    for i, row in df.iterrows():
        current_value = row['settled_as']

        if current_value == previous_value:
            consecutive_count += 1
        else:
            consecutive_count = 1

        if consecutive_count >= 1:
            if row["start_time"] in bitcoin_data.index:
                predicted_value = 'Yes' if current_value == 'Yes' else 'No'
                # predicted_value = 'Yes' if bitcoin_data.loc[row["start_time"],"open"] >= row["target_price"] else "No"
                next_index = i + 1

                if next_index < len(df):
                    actual_next_value = df.iloc[next_index]['settled_as']
        

                    if predicted_value == actual_next_value:
                        score += 4
                        # print(f"Profit")
                    else:
                        score -= 5
                        # print(f"Loss")
                    max_profit = max(max_profit, score)
                    max_loss = min(max_loss, score)

            # consecutive_count = 0
        previous_value = current_value

    return score, max_profit, max_loss

# Example usage
csv_file = 'bitcoin_data.csv'  # Path to your CSV file
dates = ['2024-07-12','2024-07-13','2024-07-14','2024-07-15','2024-07-16','2024-07-17','2024-07-18','2024-07-19','2024-07-20','2024-07-21','2024-07-22','2024-07-23','2024-07-24','2024-07-25','2024-07-26','2024-07-27','2024-07-28','2024-07-29','2024-07-30']  # Input date
for date_str in dates:
    score, max_profit, max_loss = calculate_score(csv_file, date_str)
    print(f"The final score for the date {date_str} is: {score}. Max Profit : {max_profit}, Max Loss : {max_loss}")