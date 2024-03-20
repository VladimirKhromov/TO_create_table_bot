from __future__ import annotations

import threading
from tkinter import *
from tkinter import ttk

from main import run_bot, process_bot, stop_bot

# root
root = Tk()
root.title("Телеграм-Бот обработки файлов ТО")
root.geometry("450x250")


# root.iconbitmap('icon.ico')

# pressing button

def process():
    if button_run["text"] != "Обработка":
        button_run["text"] = "Обработка"
        bot_process = threading.Thread(target=process_bot)
        bot_process.start()


def quit_button():
    stop_bot()
    root.destroy()


# label text
label_text = """
1. Запустите бота.
2. В 1С выбрать дату ТО и нажать "Сохранить в Excel"
3. Сохраненный файл отправить Боту в Телеграм.
4. Дождаться окончания обработки и выйти из приложения."""

# window's buttons and labels

button_run = ttk.Button(text="Обработать Файлы", command=process)
button_run.pack(anchor="n", pady=10)

label = ttk.Label(text=label_text)
label.pack(anchor="center")

button_quit = ttk.Button(text="Выход", command=quit_button)
button_quit.pack(anchor="s", pady=10)

# run
if __name__ == "__main__":
    try:
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
        root.mainloop()
    finally:
        stop_bot()
