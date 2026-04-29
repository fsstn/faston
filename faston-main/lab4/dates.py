from datetime import datetime, timedelta

# 1. Subtract five days from current date
# datetime.now() gives current date and time
today = datetime.now()

# timedelta(days=5) represents 5 days
five_days_ago = today - timedelta(days=5)

print("1) Subtract 5 days")
print("Today:", today)
print("5 days ago:", five_days_ago)


# 2. Print yesterday, today, tomorrow
# We use timedelta to move 1 day back or forward
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("\n2) Yesterday, Today, Tomorrow")
print("Yesterday:", yesterday.date())   # .date() shows only date
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())


# 3. Drop microseconds from datetime
# .replace(microsecond=0) removes microseconds part
no_microseconds = today.replace(microsecond=0)

print("\n3) Remove microseconds")
print("With microseconds:", today)
print("Without microseconds:", no_microseconds)


# 4. Calculate difference between two dates in seconds
# Example dates (you can change them)
date1 = datetime(2025, 5, 10, 12, 0, 0)
date2 = datetime(2025, 5, 12, 14, 30, 0)

# Subtracting dates gives timedelta
# .total_seconds() converts it into seconds
difference_seconds = abs((date2 - date1).total_seconds())

print("\n4) Difference between two dates")
print("Date 1:", date1)
print("Date 2:", date2)
print("Difference in seconds:", difference_seconds)