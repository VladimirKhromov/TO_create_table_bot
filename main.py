from __future__ import annotations

from datetime import datetime, timedelta

import xlrd
from openpyxl import Workbook

#  time settings
today = datetime.now()
tomorrow = datetime.now() + timedelta(days=1)
DATE_TO = tomorrow.strftime("%d.%m")
DATE_CALL = today.strftime("%d.%m")


# Класс работы с водителем

class Driver:
    """ Класс представления водителя. """

    def __init__(self, car_number, time):
        self.car_number = car_number
        self.time = time
        self.fio = None
        self.phone_number = None

    def get_driver_info(self):
        info = [self.time, self.car_number, self.fio, self.phone_number]
        return tuple([i for i in info if i])


# работа с телеграм ботом

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


if __name__ == '__main__':
    check_correct_date()
    res = get_time_car_list(sh)
    print(res)
    write_to_driver_table(res, "dj")
