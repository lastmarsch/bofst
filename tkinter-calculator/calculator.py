# Calculates hours worked per number of days
import datetime

import numpy as np

def count_hours(coeff, days, part_time = 8):
  return coeff * part_time * days

# Get date from the previous month
def previous_month(date, day):
  new_month, new_year = (
    date.month-1,
    date.year
  ) if date.month != 1 else (12, date.year-1)
  new_date = date.replace(day=day, month=new_month, year=new_year)
  return new_date

def calculate_working_days(month, year, half=1):
  # Calculate working days in the current date
  if half == 1:
    date = datetime.date(year, month, 15)
    prev_date = previous_month(date, 26)
    busy_days = np.busday_count(
      prev_date,
      date
    )
  else:
    busy_days = np.busday_count(
      datetime.date(year, month, 16),
      datetime.date(year, month, 25),
    )
  # print(f"Busy days: {busy_days}")
  return busy_days

def calculate(coeff, month, year, half=1, part_time = 8):
  busy_days = calculate_working_days(month, year, half)
  return count_hours(coeff, busy_days, part_time)