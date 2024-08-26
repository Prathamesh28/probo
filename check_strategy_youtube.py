import pandas as pd

def calculate_score(csv_file, date_str, video_name):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Convert the 'start_time' column to datetime
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # Filter data based on the input date
    date = pd.to_datetime(date_str)

    df = df[df['video_name'] == video_name]
    
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

        if consecutive_count >= 2:
            predicted_value = 'Yes' if current_value == 'Yes' else 'No'
            next_index = i + 1

            if next_index < len(df):
                actual_next_value = df.iloc[next_index]['settled_as']
    

                if predicted_value == actual_next_value:
                    score += 4
                    print(f"Profit")
                else:
                    score -= 5
                    print(f"Loss")
                max_profit = max(max_profit, score)
                max_loss = min(max_loss, score)

        previous_value = current_value

    return score, max_profit, max_loss

# Example usage
csv_file = 'youtube_data.csv'  # Path to your CSV file
date_str = '2024-07-15'  # Input date
video_name = "MrBeast - 50 YouTubers Fight"
score, max_profit, max_loss = calculate_score(csv_file, date_str, video_name)
print(f"The final score for the date {date_str} is: {score}. Max Profit : {max_profit}, Max Loss : {max_loss}")