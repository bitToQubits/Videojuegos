from tkinter import *
import datetime


root = Tk()
root.title("Rage")
root.geometry("500x300")

username_label = Label(root, text="Username: ")
username_label.grid(row=0, column=0, padx=10, pady=10)

name_label = Label(root, text="Nombre Real: ")
name_label.grid(row=1, column=0, padx=10, pady=10)

date_label = Label(root, text="Fecha: ")
date_label.grid(row=2, column=0, padx=10, pady=10)

score_label = Label(root, text="Puntuación: ")
score_label.grid(row=3, column=0, padx=10, pady=10)

username_text = StringVar()
name_text = StringVar()
score_text = StringVar()

username_entry = Entry(root, textvariable=username_text, state="readonly")
username_entry.grid(row=0, column=1, padx=10, pady=10)

name_entry = Entry(root, textvariable=name_text, state="readonly")
name_entry.grid(row=1, column=1, padx=10, pady=10)

score_entry = Entry(root, textvariable=score_text, state="readonly")
score_entry.grid(row=3, column=1, padx=10, pady=10)


def update_date():
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    date_label.config(text="Fecha: " + date)


update_date()

keyboard = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"]
]

for row in range(len(keyboard)):
    for col in range(len(keyboard[row])):
        key = keyboard[row][col]
        key_label = Label(root, text=key, font=("Helvetica", 20), padx=10, pady=10)
        key_label.grid(row=row + 4, column=col, padx=5, pady=5)


def select_key(event):
    widget = root.focus_get()
    if widget == username_entry or widget == name_entry:
        current_text = widget.get()
        widget.delete(0, END)
        widget.insert(0, current_text + event.keysym)
    elif widget == score_entry:
        score_text.set(score_text.get() + event.keys)

    root.mainloop()