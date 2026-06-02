from datetime import datetime, timedelta
import sqlite3

class AltaiBookingSystem:
    def __init__(self, prices_data):
        self.prices = prices_data
        
        # Подключаемся к базе данных
        self.conn = sqlite3.connect('altai_resort.db')
        self.cursor = self.conn.cursor()
        
        # Создаём таблицу для броней
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                room_type TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def is_available(self, start_date, end_date, room_type):
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        self.cursor.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE room_type = ?
            AND start_date < ?
            AND end_date > ?
        """, (room_type, end_str, start_str))
        
        count = self.cursor.fetchone()[0]
        return count == 0

    def book_room(self, start_date, end_date, room_type):
        # Проверка доступности
        if not self.is_available(start_date, end_date, room_type):
            return "Номер занят на эти даты"

        # Проверка существования категории
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

        # Сохраняем бронь в базу данных
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO bookings (room_type, start_date, end_date) VALUES (?, ?, ?)",
            (room_type, start_str, end_str)
        )
        self.conn.commit()

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

    total = booking_system.book_room(date_start, date_end, room_type)

    if isinstance(total, str):
        print(total)
    elif total is None:
        print("Ошибка: такой категории нет. Выберите из списка.")
    elif total == -1:
        print("Ошибка: дата выезда должна быть позже даты заезда.")
    else:
        print(f"Итоговая цена: {total} рублей")

except ValueError:
    print("Ошибка: даты должны быть в формате ДД.ММ.ГГГГ. Например: 15.06.2025")
