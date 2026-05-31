from datetime import datetime, timedelta

# запрашиваем данные у пользователя
start = input("Введите дату заезда: ")
end = input("Введите дату выезда: ")

date_start = datetime.strptime(start, "%d.%m.%Y")
date_end = datetime.strptime(end, "%d.%m.%Y")

# считаем количество дней
difference = date_end - date_start
print(f"Разница: {difference.days} дней")

# считаем цену проживания
standard_price = 5540
weekend_price = 6900
total_cost = 0
current_day = date_start

if difference.days > 0:
    while current_day < date_end:
        day_number = current_day.weekday()
        if day_number == 4 or day_number == 5:
            total_cost = total_cost + weekend_price
        else:
            total_cost = total_cost + standard_price
        current_day = current_day + timedelta(days=1)
    print(total_cost)
elif difference.days <= 0:
    print("Неправильно введены даты")
