from datetime import datetime, timedelta

try:
    # запрашиваем данные у пользователя
    start = input("Введите дату заезда: ")
    end = input("Введите дату выезда: ")
    
    date_start = datetime.strptime(start, "%d.%m.%Y")
    date_end = datetime.strptime(end, "%d.%m.%Y")
    
    # считаем количество дней
    difference = date_end - date_start
    print(f"Разница: {difference.days} дней")
    
    # считаем цену проживания
    prices = {
        "Эко-палатка": {"weekday": 4000, "weekend": 4600},
        "Стандарт": {"weekday": 5800, "weekend": 6400},
        "Джуниор сюит": {"weekday": 7500, "weekend": 8100},
        "Люкс": {"weekday": 8500, "weekend": 9100},
        "Апартаменты": {"weekday": 10000, "weekend": 11000},
        "Апартаменты семейные": {"weekday": 15000, "weekend": 20000}
    }
    print("Выберете категорию номера: Эко-палатка, Стандарт, Джуниор сюит, Люкс, Апартаменты, Апартаменты семейные")
    room_type = input("Категория номера: ")
    
    if room_type in prices:
        total_cost = 0
        current_day = date_start
        weekday_price = prices[room_type]["weekday"]
        weekend_price = prices[room_type]["weekend"]
        
        if difference.days > 0:
            while current_day < date_end:
                day_number = current_day.weekday()
                if day_number == 4 or day_number == 5:
                    total_cost = total_cost + weekend_price
                else:
                    total_cost = total_cost + weekday_price
                current_day = current_day + timedelta(days=1)
            print( f"Итоговая цена: {total_cost}")
        elif difference.days <= 0:
            print("Неправильно введены даты")
    else:
        print("Такой категории нет. Выберите из списка.")
        
except ValueError:
    print("Ошибка: даты должны быть в формате ДД.ММ.ГГГГ") 
