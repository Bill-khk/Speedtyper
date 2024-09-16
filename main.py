import word
import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.title('Speed typer game')
root.geometry('700x700')
root.configure(bg='light grey')

bg_color = 'light grey'
bg_color2 = 'white'  # Use this to vizualise widget layout


def home():
    frame1 = tk.Frame(root, width=200, height=100, bg=bg_color2)
    frame1.pack()
    title_label = tk.Label(root, text='Speed Typer Game', bg=bg_color2, font=("Arial", "28"))
    title_label.pack()
    description_label = tk.Label(root, text='Type words the fastest you can !', bg=bg_color2,
                                 font=("Arial", "14", "italic"))
    description_label.pack()
    frame2 = tk.Frame(root, width=200, height=100, bg=bg_color2)
    frame2.pack()

    style = ttk.Style()
    style.configure(style='Primary.Outline.TButton', font=('Helvetica', 25))
    btn = ttk.Button(command=playing, text='Play !', style='Primary.Outline.TButton')
    btn.pack()


def playing():
    # remove all widget
    for widget in root.pack_slaves():
        widget.destroy()

    # Windows layout
    frame3 = tk.Frame(root, width=200, height=250, bg=bg_color2)
    frame3.pack()
    word_label = tk.Label(root, text='word', bg=bg_color2, font=("Arial", "28"))
    word_label.pack()

    game_list = word.extract_json_word(5, 'words/words_dictionary.json')
    for i in range(10):
        toType = word.select_random(game_list)
        # Update windows
        word_label.configure(text=toType)
        word_label.update()
        # Play
        next_word = False
        while next_word == False:
            next_word = word.play2(toType)[0]


home()
root.mainloop()

# ---------------------- Main---------------------
# test =
# print(test)
# word.play2(test)
