import os
import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
        data_field = data.get('Data')
        if data_field:
            with open(csv_file_path, 'w', newline='', encoding='utf8') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write the header
                csv_writer.writerow(['time', 'high', 'low', 'open', 'close', 'volumeto'])
                # Write the data rows
                for entry in data_field:
                    csv_writer.writerow([entry['time'], entry['high'], entry['low'], entry['open'], entry['close'], entry['volumeto']])
        else:
            print(f"No 'Data' field found in {json_file_path}")

# Directory containing the JSON files
json_dir = './data'
csv_dir = './csv_data'

# Ensure the csv_data directory exists
os.makedirs(csv_dir, exist_ok=True)

# Convert each JSON file to a CSV file
for json_file_name in os.listdir(json_dir):
    if json_file_name.endswith('.json'):
        json_file_path = os.path.join(json_dir, json_file_name)
        csv_file_name = json_file_name.replace('.json', '.csv')
        csv_file_path = os.path.join(csv_dir, csv_file_name)
        json_to_csv(json_file_path, csv_file_path)
