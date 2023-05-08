import tkinter as tk


root = tk.Tk()
root.configure(bg='black')

image = tk.PhotoImage(file='elison pixel (1).png')

from tkinter.ttk import Style, Label

style = Style()
style.configure('Neon.TLabel', foreground='white', font=('Helvetica', 30, 'bold'),
                anchor='center', borderwidth=0, padding=(10, 10, 10, 10),
                background='black')

text = Label(root, text="Gracias por jugar nuestro Arcade. Hasta la próxima!",
             image=image, compound='left', style='Neon.TLabel',)

text.pack(pady=25)




from itertools import cycle

colors = cycle(['white', 'magenta', 'blue', 'green', 'yellow', 'red'])
def animate():
    text.configure(foreground=next(colors))
    root.after(100, animate)

animate()

root.mainloop()