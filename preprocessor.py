import re
import pandas as pd


def preprocessor(text_data):
    # Regular expression pattern to extract information
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}) - ([^:]+): (.+)"

    # Lists to store extracted information
    dates = []
    users = []
    messages = []

    # Loop through each line and extract information using regular expression
    for line in text_data.split('\n'):
        match = re.match(pattern, line)
        if match:
            date, user, message = match.groups()
            dates.append(date)
            users.append(user)
            messages.append(message)

    # Create DataFrame using the lists
    data = {
        'date': dates,
        'user': users,
        'message': messages
    }
    df = pd.DataFrame(data)

    # Convert the 'date' column to datetime data type (format: %m/%d/%y, %H:%M)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    return df




