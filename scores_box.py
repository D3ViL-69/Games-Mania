from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Scores")
root.geometry("500x400")

main_frame = Frame(root, background = "yellow")
main_frame.pack(fill = BOTH, expand = 1)

content = Label(main_frame, padx = 40, pady = 10, relief = SUNKEN, borderwidth = 4, fg = "black")
content.pack(anchor = "ne", pady = 10, padx = 20)

v = Scrollbar(content)
v.pack( side = RIGHT, fill = Y)

t = Text(content, width = 30, height = 15, wrap = NONE, yscrollcommand = v.set)

for i in range(20):
    t.insert(END, "Text\n")

t.pack(side = TOP, fill = X)

v.config(command = t.yview)
root.mainloop()
