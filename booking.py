from datetime import datetime, timedelta

class AltaiBookingSystem:
    def __init__(self, prices_data):
        self.prices = prices_data

    def calculate_total_cost(self, start_date, end_date, room_type):
        if room_type not in self.prices:
            return None

        weekday_price = self.prices[room_type]["weekday"]
        weekend_price = self.prices[room_type]["weekend"]

        difference = end_date - start_date

        if difference.days <= 0:
            return -1

        total_cost = 0
        current_day = start_date

        while current_day < end_date:
            day_number = current_day.weekday()
            if day_number == 4 or day_number == 5:
                total_cost = total_cost + weekend_price
            else:
                total_cost = total_cost + weekday_price
            current_day = current_day + timedelta(days=1)

        return total_cost

prices = {
    "Эко-палатка": {"weekday": 4000, "weekend": 4600},
    "Стандарт": {"weekday": 5800, "weekend": 6400},
    "Джуниор сюит": {"weekday": 7500, "weekend": 8100},
    "Люкс": {"weekday": 8500, "weekend": 9100},
    "Апартаменты": {"weekday": 10000, "weekend": 11000},
    "Апартаменты семейные": {"weekday": 15000, "weekend": 20000}
}

booking_system = AltaiBookingSystem(prices)

try:
    start = input("Введите дату заезда (ДД.ММ.ГГГГ): ")
    end = input("Введите дату выезда (ДД.ММ.ГГГГ): ")

    date_start = datetime.strptime(start, "%d.%m.%Y")
    date_end = datetime.strptime(end, "%d.%m.%Y")

    print("Доступные категории: Эко-палатка, Стандарт, Джуниор сюит, Люкс, Апартаменты, Апартаменты семейные")
    room_type = input("Введите категорию номера: ")

    total = booking_system.calculate_total_cost(date_start, date_end, room_type)

    if total is None:
        print("Ошибка: такой категории нет. Выберите из списка.")
    elif total == -1:
        print("Ошибка: дата выезда должна быть позже даты заезда.")
    else:
        print(f"Итоговая цена: {total} рублей")

except ValueError:
    print("Ошибка: даты должны быть в формате ДД.ММ.ГГГГ. Например: 15.06.2025")
