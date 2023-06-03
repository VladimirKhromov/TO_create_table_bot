from __future__ import annotations

from tkinter import *
from tkinter import ttk

# from main import run_bot

# требуется многопоточность, поскольку запуск бота занимает целый процесс
# требуется проверить, работает ли бот корректно при заходе/ выходе
# возможно при запуске опять обрабатывает файл результата



# root
root = Tk()
root.title("Телеграм-Бот обработки файлов ТО")
root.geometry("450x250")


# pressing button
def pressing_start_button():
    button_run["text"] = "Запущен"
    if button_run["text"] != "Запущен":
        # run_bot()
        print("1")

# label text
label_text = """
1. Запустите бота.
2. В 1С выбрать дату ТО и нажать "Сохранить в excel"
3. Сохраненный файл отправить Боту в Телеграм.
4. Дождаться окончания обработки и выйти из приложения."""


# window's buttons and labels

button_run = ttk.Button(text="Запустить", command=pressing_start_button)
button_run.pack(anchor="n", pady=10)

label = ttk.Label(text=label_text)
label.pack(anchor="center")

button_quit = ttk.Button(text="Выход", command=root.destroy)
button_quit.pack(anchor="s", pady=50)

# run
if __name__ == "__main__":
    root.mainloop()
