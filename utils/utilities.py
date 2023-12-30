from datetime import datetime
from flask import jsonify, render_template

def calculate_duration(start_date_str, end_date_str):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%d-%m-%Y %H:%M')
    end_date = datetime.strptime(end_date_str, '%d-%m-%Y %H:%M')

    # Calculate the duration
    duration = end_date - start_date

    # Extract days and minutes from the duration
    days = duration.days
    minutes = duration.seconds // 60

    return days, minutes

def validate_date_time(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, '%d-%m-%Y %H:%M')
        end_date = datetime.strptime(end_date, '%d-%m-%Y %H:%M')
    except ValueError as e:
        print(f"Oops!! got invalid date time: {e}")
        return jsonify({'error': "Oops!! got invalid date time"}), 400
    else:
        if start_date>end_date:
            return render_template('error.html', message='End date time must be after start date time', status_code=404), 404