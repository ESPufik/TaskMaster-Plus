import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import winsound
from datetime import datetime, timedelta
import threading
import subprocess


class Task:
    def __init__(self, name, start_time, end_time, sound_file=None, exe_path=None, close_after=False):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.sound_file = sound_file
        self.exe_path = exe_path
        self.close_after = close_after


def add_task():
    name = name_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    sound_file = sound_file_var.get()
    exe_path = exe_path_var.get()
    close_after = close_var.get()

    # Проверяем, что все поля заполнены
    if name and start_time and end_time:
        tasks.append(Task(name, start_time, end_time, sound_file, exe_path, close_after))
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields")


def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, f"{task.name} - {task.start_time} - {task.end_time}")


def check_time():
    current_time = datetime.now().strftime("%H:%M")
    for task in tasks:
        if current_time == task.start_time:
            messagebox.showinfo("Notification", f"Time to start task: {task.name}")
            play_notification_sound(task.sound_file)  # Воспроизводим звук
            if task.exe_path:
                open_exe(task.exe_path)
        elif current_time == task.end_time:
            messagebox.showinfo("Notification", f"Time to end task: {task.name}")
            play_notification_sound(task.sound_file)  # Воспроизводим звук
            if task.exe_path and task.close_after:
                open_exe(task.exe_path)
                root.quit()  # Закрываем приложение
            elif task.exe_path:
                open_exe(task.exe_path)
    root.after(60000, check_time)  # Проверяем время каждую минуту


def play_notification_sound(sound_file):
    if sound_file:
        try:
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        except Exception as e:
            print(f"Error playing sound: {e}")


def test_sound():
    messagebox.showinfo("Test Notification", "This is a test notification!")
    play_notification_sound(sound_file_var.get())


def browse_sound_file():
    filename = filedialog.askopenfilename()
    sound_file_var.set(filename)


def browse_exe_file():
    filename = filedialog.askopenfilename()
    exe_path_var.set(filename)


def close_app():
    root.quit()


def set_light_theme():
    root.config(bg="white")
    style.theme_use("default")


def set_dark_theme():
    root.config(bg="#1e1e1e")
    style.theme_use("clam")


def run_background():
    threading.Thread(target=check_time, daemon=True).start()


def open_github():
    webbrowser.open("https://github.com/ESPufik")


root = tk.Tk()
root.title("Daily - For You <3")  # Изменяем заголовок приложения

tasks = []

name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, sticky="w")

name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

start_time_label = tk.Label(root, text="Start time:")
start_time_label.grid(row=1, column=0, sticky="w")

start_time_entry = tk.Entry(root)
start_time_entry.grid(row=1, column=1)

end_time_label = tk.Label(root, text="End time:")
end_time_label.grid(row=2, column=0, sticky="w")

end_time_entry = tk.Entry(root)
end_time_entry.grid(row=2, column=1)

sound_file_label = tk.Label(root, text="Notification sound file:")
sound_file_label.grid(row=3, column=0, sticky="w")

sound_file_var = tk.StringVar()
sound_file_entry = tk.Entry(root, textvariable=sound_file_var)
sound_file_entry.grid(row=3, column=1)

browse_sound_button = tk.Button(root, text="Browse", command=browse_sound_file)
browse_sound_button.grid(row=3, column=2)

exe_path_label = tk.Label(root, text=".exe file path:")
exe_path_label.grid(row=4, column=0, sticky="w")

exe_path_var = tk.StringVar()
exe_path_entry = tk.Entry(root, textvariable=exe_path_var)
exe_path_entry.grid(row=4, column=1)

browse_exe_button = tk.Button(root, text="Browse", command=browse_exe_file)
browse_exe_button.grid(row=4, column=2)

close_var = tk.BooleanVar()
close_check = tk.Checkbutton(root, text="Close application after time expires", variable=close_var)
close_check.grid(row=5, columnspan=3)

add_button = tk.Button(root, text="Add task", command=add_task)
add_button.grid(row=6, columnspan=3)

task_list = tk.Listbox(root, width=50)
task_list.grid(row=7, columnspan=3)

update_task_list()

test_button = tk.Button(root, text="Test notification", command=test_sound)
test_button.grid(row=8, column=0, sticky="sw")  # Изменяем позицию кнопки

version_button = tk.Button(root, text="Version 1.0.0", command=open_github)
version_button.grid(row=6, column=2, sticky="se")  # Добавляем кнопку и устанавливаем ее позицию

style = ttk.Style()
style.theme_use("default")

# Создание меню
menubar = tk.Menu(root)
root.config(menu=menubar)

theme_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light", command=set_light_theme)
theme_menu.add_command(label="Dark", command=set_dark_theme)

menubar.add_command(label="Exit", command=close_app)

# Надпись
label = tk.Label(root, text="by Kapranov - With Love <3", anchor="se", foreground="gray")
label.place(relx=1, rely=1, anchor="se")

run_background()  # Запускаем функцию в фоновом потоке

root.mainloop()
