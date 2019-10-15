import csv
from datetime import datetime, timedelta
from filelock import FileLock

def get_data(date_start, date_end):
    """
    Get meter usage data for between the start and end date
    """
    # csv filename
    filename = "meterusage.csv"
    # user specified start date
    start = datetime.strptime(date_start, '%Y-%m-%d')
    # user specified end date
    end = datetime.strptime(date_end, '%Y-%m-%d')
    # add 1 day to end date to make it inclusive
    end += timedelta(days=1, minutes=-15)
    # initialize return dictionary
    usage_dict = {}
    # open csv file
    with FileLock(filename): # secure against multiple threads reading from the same file at the same time
        with open(filename, 'r') as meterusage_file:
            meterusage_reader = csv.reader(meterusage_file)
            # skip header row
            next(meterusage_reader)
            # loop through all rows
            for row in meterusage_reader:
                datetime_obj = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                # if datetime falls within range
                if datetime_obj >= start and datetime_obj <= end:
                    date = datetime_obj.date().strftime("%Y-%m-%d")
                    time = datetime_obj.time().strftime("%H:%M:%S")
                    # add to dictionary
                    if date in usage_dict:
                        usage_dict[date].append({'time': time, 'value': row[1]})
                    else:
                        usage_dict[date] = [{'time': time, 'value': row[1]}]
    # return dictionary formatted as a string
    if not usage_dict:
        return str("")
    return str(usage_dict)
