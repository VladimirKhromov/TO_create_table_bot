from __future__ import annotations

from datetime import datetime, timedelta
from functools import wraps
from urllib import request

import telebot  # pyTelegramBotAPI
import xlrd  # read old version .xlsx files
from openpyxl import Workbook  # create and save .xlsx file
from telebot.types import InputFile

from settings import token, users_id

#  time settings
today = datetime.now()
tomorrow = datetime.now() + timedelta(days=1)
DATE_TO = tomorrow.strftime("%d.%m")
DATE_CALL = today.strftime("%d.%m")


# EXCEL

def _get_car_number(string: str) -> str:
    """ Find and return car number in str. """
    string = string.split()
    for word in string:
        if word[-1] in ("7", "9"):
            result_car = word
            return result_car
    return ""


def get_time_car_list(sheet: Workbook.active) -> list[list[str]]:
    """ """
    result_list = []

    for row in range(2, sheet.ncols - 1):
        # get time
        hour = int(sheet.cell_value(1, row)) if sheet.cell_value(1, row) != 42 else int(sheet.cell_value(1, row - 1))
        minute = int(sheet.cell_value(2, row))
        time = f'{hour:02d}:{minute:02d}'

        # get car
        for i in (3, 4, 5):
            string = sheet.cell_value(i, row)  # sheet --> sh
            if string != 42:  # xlrd print "42" in empty cell
                result_car = _get_car_number(string)
                result_list.append([time, result_car])

    return result_list


def write_to_driver_table(time_car_list: list[list[str]], name: str) -> None:
    # create file
    out_book = Workbook()
    sheet = out_book.active

    # create table
    for i in range(1, len(time_car_list) + 1):
        sheet.cell(column=1, row=i).value = DATE_TO
        sheet.cell(column=2, row=i).value = time_car_list[i - 1][0]
        sheet.cell(column=3, row=i).value = time_car_list[i - 1][1]
        sheet.cell(column=4, row=i).value = ''
        sheet.cell(column=5, row=i).value = ''
        sheet.cell(column=6, row=i).value = name
        sheet.cell(column=7, row=i).value = DATE_CALL

    # save table
    out_book.save("result.xlsx")
    out_book.close()


# TELEBOT

bot = telebot.TeleBot(token)


def private_access():
    """ decorate for user verification. """

    def deco_restrict(func):
        @wraps(func)
        def f_restrict(message, *args, **kwargs):
            user = message.from_user.id
            if user in users_id:
                return func(message, *args, **kwargs)
            else:
                bot.reply_to(message, text=f'Who are you? Keep on walking...')
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


# Handle sent .xlsx document
@bot.message_handler(func=lambda message: True, content_types=['document'])
@private_access()
def default_command(message):
    file_name = message.document.file_name
    file_extension = file_name.split(".")[-1]
    if file_extension.lower() != "xlsx":
        bot.send_message(message.chat.id, f"Файл {file_name} не является файлом xlsx, загрузите правильный файл")
        return
    bot.send_message(message.chat.id, f"Файл {file_name} получен")

    # open file
    file_info = bot.get_file(message.document.file_id)
    xlsx_path = f'https://api.telegram.org/file/bot{token}/{file_info.file_path}'
    file, headers = request.urlretrieve(xlsx_path)

    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)

    # check_correct_date
    data_in_file = str((sheet.cell_value(0, 2)).split()[0])
    if data_in_file != tomorrow.strftime("%d.%m.%Y"):
        bot.send_message(message.chat.id,
                         "‼️❗️‼️❗️‼️❗️‼️\nДата ТО в файле и завтрашняя дата не совпадают. "
                         "Проверьте правильно ли скачан файл")

    # make result file
    res = get_time_car_list(sheet)
    write_to_driver_table(res, "")

    # return result file
    bot.send_document(
        message.chat.id,
        InputFile("result.xlsx"))


if __name__ == '__main__':
    bot.infinity_polling()  # run bot
