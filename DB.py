import sqlite3

DB_file = 'drivers.db'

# Создание общей таблицы

connect = sqlite3.connect(':memory:')


def create_DB():
    with sqlite3.connect(DB_file) as connect:
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS drivers(
        driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time VARCHAR,
        car VARCHAR,
        name_driver VARCHAR,
        phone_driver VARCHAR,       
        info_driver VARCHAR
        )""")
        cursor.execute("DELETE FROM drivers")

        cursor.execute("""CREATE TABLE IF NOT EXISTS to_drivers(
        to_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date VARCHAR, 
        time VARCHAR,
        car VARCHAR,
        name_driver VARCHAR,
        phone_driver VARCHAR,
        logist_name VARCHAR,
        date_call VARCHAR,
        info_driver VARCHAR
        )""")

        cursor.execute("DELETE FROM to_drivers")

        connect.commit()


def clear_DB():
    with sqlite3.connect(DB_file) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM drivers")
        cursor.execute("DELETE FROM to_drivers")
        connect.commit()


def update_drivers_table(car, name_driver, phone_driver, info_driver):
    with sqlite3.connect(DB_file) as connect:
        cursor = connect.cursor()
        queue = f"INSERT INTO drivers (car, name_driver, phone_driver, info_driver) VALUES {car}, {name_driver}, {phone_driver}, {info_driver}"
        cursor.execute(queue)
        connect.commit()


def update_to_drivers_table(date, time, car, name_driver, phone_driver, logist_name, date_call, info_driver):
    with sqlite3.connect(DB_file) as connect:
        cursor = connect.cursor()
        queue = f"""INSERT INTO to_drivers (date, time, car, name_driver, phone_driver, logist_name, date_call, info_driver) VALUES {date}, {time}, {car}, {name_driver}, {phone_driver}, {logist_name}, {date_call}, {info_driver}"""
        cursor.execute(queue)
        connect.commit()


if __name__ == "__main__":
    create_DB()
    clear_DB()
