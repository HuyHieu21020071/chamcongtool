import csv
import os
import sys
from datetime import datetime, timedelta


def check_in_month(param_date, input_date):
    month = input_date.month
    year = input_date.year
    if month == 1:
        last_month = datetime(year - 1, 12, 16)
        next_month = datetime(year, month, 15)
        return last_month <= param_date <= next_month
    last_month = datetime(year, month - 1, 16)
    next_month = datetime(year, month, 15)
    return last_month <= param_date <= next_month


def calculate_total_time_work(id, data_csv, month):
    total_time_worked = timedelta(hours=0, minutes=0, seconds=0)
    for row in data_csv:
        if row[1] == id and check_in_month(datetime.strptime(row[3], "%Y-%m-%d"), month):
            if row[5] == '' or row[4] == '':
                continue
            start_time_str = row[4]  # Assuming column 4 contains the start time
            end_time_str = row[5]  # Assuming column 5 contains the end time

            # Convert the time strings to datetime objects
            start_time = datetime.strptime(start_time_str, "%H:%M:%S")
            end_time = datetime.strptime(end_time_str, "%H:%M:%S")
            if start_time < datetime.strptime('08:30:00', "%H:%M:%S"):
                start_time = datetime.strptime('08:30:00', "%H:%M:%S")
            if end_time > datetime.strptime('18:00:00', "%H:%M:%S"):
                end_time = datetime.strptime('18:00:00', "%H:%M:%S")
            # Subtract time in range 12:00:00 - 13:00:00
            if start_time <= datetime.strptime('12:00:00', "%H:%M:%S") and end_time >= datetime.strptime('13:00:00', "%H:%M:%S"):
                time_worked = end_time - start_time - timedelta(hours=1)
            elif start_time <= datetime.strptime('12:00:00', "%H:%M:%S") and end_time < datetime.strptime('13:00:00', "%H:%M:%S"):
                end_time = min(end_time, datetime.strptime('12:00:00', "%H:%M:%S"))
                time_worked = end_time - start_time
            elif start_time > datetime.strptime('12:00:00', "%H:%M:%S") and end_time >= datetime.strptime('13:00:00', "%H:%M:%S"):
                start_time = max(start_time, datetime.strptime('13:00:00', "%H:%M:%S"))
                time_worked = end_time - start_time
            # Add the time_worked to the total_time_worked
            total_time_worked += time_worked

    # convert total_time_worked to hours
    total_time_worked = total_time_worked.total_seconds() / 3600
    # round to 2 decimal places
    total_time_worked = round(total_time_worked, 2)
    return total_time_worked

def FindNumber():
    highest_number = 0
    for filename in os.listdir(downloads_folder):
        if filename.startswith('TEKO_ Chấm công (') and filename.endswith(').csv'):
            # Extract the number from the filename
            try:
                number = int(filename.split('(')[1].split(')')[0])
                if number > highest_number:
                    highest_number = number
            except ValueError:
                pass  # Ignore filenames that don't match the pattern
    return highest_number

if __name__ == '__main__':
    user_home_directory = os.path.expanduser("~")

    # Construct the full path to the Downloads folder and the CSV file
    downloads_folder = os.path.join(user_home_directory, 'Downloads')
    number = FindNumber()
    csv_file_path = os.path.join(downloads_folder, f'TEKO_ Chấm công ({number}).csv')
    with open(csv_file_path, 'r') as f:
        data_csv = csv.reader(f)
        employee_id = "51180"
        input_date = datetime.strptime("2024-2", "%Y-%m")
        result = calculate_total_time_work(employee_id, data_csv, input_date)
        print(f"Total time worked for employee with ID {employee_id} is: {result} hours")
