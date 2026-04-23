from datetime import datetime, timedelta

#1
curr = datetime.now()
subtract = timedelta(days=5)
new = curr - subtract
print(f"Current Date: {curr}")
print(f"Date 5 days ago: {new}")
print()

#2
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(f"Yesterday: {yesterday}\nToday: {today}\nTomorrow: {tomorrow}")
print()

#3
today = today.strftime('%Y-%m-%d %H:%M:%S')
print(f"Today: {today}")
print()

#4
s = tomorrow - yesterday
s = s.total_seconds()
print(f"Seconds between tomorrow and yesterday: {s}")
