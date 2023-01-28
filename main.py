from __future__ import annotations
from xlrd import open_workbook # for read xlsx file
  # from openpyxl import load_workbook  # for write xlsx file


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

# работа с экселем
# file name
file = 'test.xlsx'

# open file


"""
wb = open_workbook(file)
sh = wb.sheet_by_index(0)

result_table = []
for rx in range(sh.nrows):
    result_table.append([s for s in sh.row(rx) if s != "error:42"])


print(result_table)
"""