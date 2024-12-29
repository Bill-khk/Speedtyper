import tkinter as tk
from game import Game

root = tk.Tk()
root.title('Speed typer game')
root.configure(bg='light grey')
w = 700
h = 700
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

bg_color = 'light grey'
bg_color2 = 'white'  # Use this to vizualise widget layout

game1 = Game(root)
game1.layout_home()
root.mainloop()