#1 Using AND operator
age = 19
has_id = True
print(age >= 18 and has_id)   # True


#2 Using OR operator
is_weekend = True
is_holiday = False
print(is_weekend or is_holiday)   # True


#3 Using NOT operator
is_raining = False
print(not is_raining)   # True


#4 AND with false result
score = 45
passed_exam = score >= 50
print(passed_exam and score >= 60)   # False


#5 OR with both false
has_ticket = False
has_invitation = False
print(has_ticket or has_invitation)  # False


#6 Combining operators
temperature = 30
is_summer = True
print(temperature > 25 and is_summer)  # True