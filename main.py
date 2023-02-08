from __future__ import annotations

from datetime import datetime, timedelta
from functools import wraps

import telebot
import xlrd
from openpyxl import Workbook

from settings import token, users_id

#  time settings
today = datetime.now()
tomorrow = datetime.now() + timedelta(days=1)
DATE_TO = tomorrow.strftime("%d.%m")
DATE_CALL = today.strftime("%d.%m")

# Excel work

# file name
file = 'test.xlsx'

# open file
book = xlrd.open_workbook(file)
sh = book.sheet_by_index(0)


def check_correct_date():
    if str((sh.cell_value(0, 2)).split()[0]) != tomorrow.strftime("%d.%m.%Y"):
        print("Дата ТО в файле и завтрашняя дата не совпадают. Проверьте правильно ли скачан файл")


def _get_car_number(string: str) -> str:
    string = string.split()
    for word in string:
        if word[-1] in ("7", "9"):
            result_car = word
            return result_car
    return ""


def get_time_car_list(sheet) -> list:
    result_list = []

    for row in range(2, sheet.ncols - 1):
        # get time
        hour = int(sheet.cell_value(1, row)) if sheet.cell_value(1, row) != 42 else int(sheet.cell_value(1, row - 1))
        minute = int(sheet.cell_value(2, row))
        time = f'{hour:02d}:{minute:02d}'

        # get car
        for j in (3, 4, 5):
            string = sh.cell_value(j, row)
            if string != 42:  # xlrd print "42" in empty cell
                result_car = _get_car_number(string)
                result_list.append([time, result_car])

    return result_list


def write_to_driver_table(time_car_list: list[list[str]], name: str) -> None:
    # create file
    out_book = Workbook()
    sheet = out_book.active

    # заполняем таблицу
    for i in range(1, len(time_car_list) + 1):
        sheet.cell(column=1, row=i).value = DATE_TO
        sheet.cell(column=2, row=i).value = time_car_list[i - 1][0]
        sheet.cell(column=3, row=i).value = time_car_list[i - 1][1]
        sheet.cell(column=4, row=i).value = ''
        sheet.cell(column=5, row=i).value = ''
        sheet.cell(column=6, row=i).value = name
        sheet.cell(column=7, row=i).value = DATE_CALL

    # сохраняем таблицу
    out_book.save("result.xlsx")
    out_book.close()


# работа с телеграм ботом

bot = telebot.TeleBot(token)

# Проверка пользователя
def private_access():
    def deco_restrict(f):
        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.username
            if username in users_id:
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text=f'Who are you? {username} Keep on walking...')
        return f_restrict  # true decorator
    return deco_restrict


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
@private_access()
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Бот конвертирует список авто из 1с в список для обзвона.
Просто пришлите xlsx файл из 1с мне.\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True, content_types=['document'])
@private_access()
def default_command(message):
    file_name = message.document.file_name
    file_id = message.document.file_id
    if file_name.split(".")[-1] != "xlsx":
        bot.send_message(message.chat.id, f"Файл {file_name} не является файлом xlsx, загрузите правильный файл")
        return
    bot.send_message(message.chat.id, f"Файл {file_name} {file_id} получен")

    # TO DO !!!
    # check_correct_date()
    # res = get_time_car_list(sh)
    # print(res)
    # write_to_driver_table(res, "dj")

if __name__ == '__main__':
    bot.infinity_polling()  # run bot
