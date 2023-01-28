from __future__ import annotations

from datetime import datetime, timedelta

from openpyxl import Workbook
from xlrd import open_workbook  # for read xlsx file

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
book = open_workbook(file)
sh = book.sheet_by_index(0)

def check_correct_date():
    if str((sh.cell_value(0, 2)).split()[0]) != tomorrow.strftime("%d.%m.%Y"):
        print("Дата ТО в файле и завтрашняя дата не совпадают. Проверьте правильно ли скачан файл")


def get_time_car_list(book) -> list:
    pass



def get_driver_car_list(sheet) -> list:
    sh = sheet.sheet_by_index(0)
    result_list = [[], [], [], []]

    for row in range(2, sh.ncols - 1):
        # time add
        hour = int(sh.cell_value(1, row)) if sh.cell_value(1, row) != 42 else int(sh.cell_value(1, row - 1))
        minute = int(sh.cell_value(2, row))
        result_list[0].append(f'{hour:02d}:{minute:02d}')

        # car number add
        for j in (3, 4, 5):
            result = ""
            s = sh.cell_value(j, row)
            if s != 42:
                s = s.split()
                for word in s:
                    if word[-1] in ("7", "9"):
                        result = word
                        break
            result_list[j - 2].append(result)

    return result_list


def make_result_car_table(table):
    new_table = []
    for i in range(len(table[0])):
        temp_list_number_car = []
        temp_list_number_car.clear()
        for j in (1, 2, 3):
            if table[j][i] != '':
                temp_list_number_car.append(table[j][i])

        for car in temp_list_number_car:
            new_table.append([table[0][i], car])
    return new_table


def write_to_driver_table(result_table: list[list[str]], name: str) -> None:
    # create file
    out_book = Workbook()
    sheet = out_book.active

    # заполняем таблицу
    for i in range(1, len(result_table)+1):
        sheet.cell(column=1, row=i).value = DATE_TO
        sheet.cell(column=2, row=i).value = result_table[i-1][0]
        sheet.cell(column=3, row=i).value = result_table[i-1][1]
        sheet.cell(column=4, row=i).value = ''
        sheet.cell(column=5, row=i).value = ''
        sheet.cell(column=6, row=i).value = name
        sheet.cell(column=7, row=i).value = DATE_CALL

    # сохраняем таблицу
    out_book.save("result.xlsx")
    out_book.close()


if __name__ == '__main__':
    check_correct_date()
    res = make_result_car_table(get_driver_car_list(book))
    print(res)
    write_to_driver_table(res, "dj")
