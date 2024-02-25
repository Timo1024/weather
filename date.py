from datetime import datetime

# Convert milliseconds to seconds
timestamp_seconds = 1708297200000 / 1000

# Convert to datetime
datetime_obj = datetime.utcfromtimestamp(timestamp_seconds)

print(datetime_obj)