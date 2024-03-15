import sqlite3

# Создание базы
# Удаление базы

# Заполнение таблицы TO
# Заполнение таблицы Drivers

# Создание общей таблицы

connect = sqlite3.connect(':memory:')

def create_DB():
    with

# Установить соединение с базой данных в памяти
connect = sqlite3.connect(':memory:')

# Создать курсор для выполнения SQL-запросов
cursor = connect.cursor()

# Создать таблицу
cursor.execute('''CREATE TABLE users
                  (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Вставить данные в таблицу
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))

# Сохранить изменения (хотя это необязательно для базы данных в памяти)
connect.commit()

# Выполнить запрос к базе данных
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Закрыть соединение
connect.close()
