import tkinter as tk
import tkinter.ttk as ttk


# Add button with function
def add_play(text, func):
    style = ttk.Style()
    style.configure(style='Primary.Outline.TButton', font=('Helvetica', 25))
    btn = ttk.Button(command=func, text=text, style='Primary.Outline.TButton')
    btn.pack()


# Add white space
def add_frame(parent, bg='white'):
    frame1 = tk.Frame(parent, width=200, height=100, bg=bg)
    frame1.pack()


# Add_title
def add_title(parent, text, bg='white'):
    title_label = tk.Label(parent, text=text, bg=bg, font=("Arial", "28"))
    title_label.pack()


# Add subtitle
def add_subtitle(parent, text, bg='white'):
    description_label = tk.Label(parent, text=text, bg=bg,
                                 font=("Arial", "14", "italic"))
    description_label.pack()
    return description_label


# Add text
def add_text(parent, word, color_split, bg='white'):
    t1 = word[0:color_split]
    t2 = word[color_split:]

    T = tk.Text(parent, height=6, width=len(word) + 10, background=bg)
    T.tag_configure("center", justify='center')
    T.tag_configure("green", foreground='green', font=("Helvetica", "25"))
    T.tag_configure('black', foreground='black', font=("Helvetica", "25"))

    T.insert(tk.END, t1)
    T.insert(tk.END, t2)

    # Number of letter to color
    tapped = color_split

    T.tag_add("green", f"1.0", f"1.{tapped}")
    T.tag_add('black', f"1.{tapped}", "end")
    T.tag_add("center", "1.0", "end")
    T.pack()
    return T


def update_text(parent, label, word, color_split):
    label.delete('1.0', 'end')  # delete previous word
    label.config(width=len(word) + (2 * len(word)))  # Update label windows size
    t1 = word[0:color_split]
    t2 = word[color_split:]

    label.insert(tk.END, t1)
    label.insert(tk.END, t2)
    # Number of letter to color
    tapped = color_split
    label.tag_add("green", f"1.0", f"1.{tapped}")
    label.tag_add('black', f"1.{tapped}", "end")
    label.tag_add("center", "1.0", "end")
    parent.update()

# Destroy all the current layout
def remove_all_w(root):
    for widget in root.pack_slaves():
        widget.destroy()
