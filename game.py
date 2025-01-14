import time

import _tkinter

import word
import tk_layout
import tkinter as tk
import threading
from functools import partial
import keyboard

LIFE = 2
DEFAULT_TIME = 10
NB_WORD = 4


class Game:

    def __init__(self, root, nbWord=NB_WORD):
        # Game parameters
        self.nbWord = nbWord
        self.cLife = LIFE  # Current life
        self.remaining_time = DEFAULT_TIME
        # Game variable
        self.totalTime = 0
        self.current_word_index = 0
        self.words_to_type = []
        self.keys_pressed = ""
        # Graphic element
        # Stock Graphic_Element - [0:Lives_count, 1:Word_count, 2:Clock, 3:Text_label]
        self.GE = []
        self.root = root
        # Threading management
        self.stop_CD_flag = threading.Event()
        self.next_word_flag = threading.Event()
        self.restart_CD_flag = threading.Event()

    def game_init(self):
        self.cLife = LIFE
        self.remaining_time = DEFAULT_TIME
        self.totalTime = 0
        self.current_word_index = 0
        self.keys_pressed = ""
        self.words_to_type = []
        self.next_word_flag.clear()
        self.stop_CD_flag.clear()
        self.GE = []

    #  --------------------------------Custom layout creation-----------------------------------------

    #  Set up the home menu layout
    def layout_home(self):
        tk_layout.add_frame(self.root)
        tk_layout.add_title(self.root, 'Speed Typer Game')
        tk_layout.add_subtitle(self.root, 'Type words the fastest you can !')
        tk_layout.add_frame(self.root)
        tk_layout.add_play('Play !', self.playing)
        tk_layout.add_frame(self.root)

    # Set up the end game layout
    def layout_end(self, root, timerCode):
        tk_layout.remove_all_w(root)
        tk_layout.add_frame(root)
        if timerCode == -1:
            tk_layout.add_subtitle(root, f'You exit the game !')
        elif timerCode != -100:
            tk_layout.add_subtitle(root, f'You finished in {timerCode} seconds !')
        else:
            tk_layout.add_subtitle(root, f'No more lives, you lost !')
        tk_layout.add_frame(root)
        button = tk_layout.add_play('Play again !', self.playing)
        # Manage the countdown syn for fast exit and replay
        button.config(state=tk.DISABLED)
        self.root.update()
        time.sleep(1)
        button.config(state=tk.NORMAL)

        # Ensure listener stops when the Tkinter window is closed
        # root.protocol("WM_DELETE_WINDOW", app.stop_listener)
        root.mainloop()  # the remove_w function also remove the mainloop parameter

    #  Set up the playing menu layout
    def layout_game(self):
        tk_layout.remove_all_w(self.root)
        tk_layout.add_frame(self.root)
        tk_layout.add_frame(self.root)
        lives_count = tk_layout.add_subtitle(self.root, f'Lives :{self.cLife}/{LIFE}')
        word_count = tk_layout.add_subtitle(self.root, 'Words :1/5')
        tk_layout.add_frame(self.root)
        clock = tk.Label(self.root, text=str(f'Time left : {DEFAULT_TIME}'))
        clock.pack()
        text = tk_layout.add_text(self.root, '', 0)
        text.pack()
        return lives_count, word_count, clock, text

    def countdown(self, parent, label, duration=DEFAULT_TIME):
        if self.stop_CD_flag.is_set():  # Stop the countdown
            print('Stop Countdown')
            self.totalTime += duration
            self.stop_CD_flag.clear()
            if self.restart_CD_flag.is_set(): # Start the Countdown for the next word
                self.countdown(self.root, self.GE[2], DEFAULT_TIME)

            return
        elif duration <= 0:  # Time's up
            print('Next Word')
            self.stop_CD_flag.clear()
            self.totalTime += 10
            # Prepare the next word
            self.next_word_flag.set()
            self.cLife -= 1
            self.GE[0].config(text=f'Lives :{self.cLife}/{LIFE}')
            self.root.update()
            self.prepare_next_word()
            return
        else:
            try:
                label.config(text=f'Time left : {duration}')
            except _tkinter.TclError:
                print('No more label for countdown')
                return

            self.root.update()
            self.root.after(1000, partial(self.countdown, parent=parent, label=label, duration=duration - 1))

    def playing(self):
        # -------------------------Game Init---------------------------
        self.game_init()
        game_list = word.extract_json_word(5, 'words/words_dictionary.json')
        list_to_type = []
        for i in range(self.nbWord):
            list_to_type.append(word.select_random(game_list))
        layout_return = self.layout_game()
        self.GE = list(layout_return)  # Graphic_Element - [0:Lives_count, 1:Word_count, 2:Clock, 3:Text_label]
        self.words_to_type = list_to_type

        # -------------------------Playing---------------------------
        # Display the first word
        self.update_game_ui()
        # Start countdown for the first word
        self.countdown(self.root, self.GE[2], self.remaining_time)
        # Bind keys for input handling
        self.root.bind("<Key>", lambda event: self.handle_keypress(event))

    # Function to trace word to type and update
    def update_game_ui(self):
        current_word = self.words_to_type[self.current_word_index]
        self.GE[1].configure(text=f'Words :{self.current_word_index + 1}/{self.nbWord}')
        tk_layout.update_text(self.root, self.GE[3], current_word, len(self.keys_pressed))
        self.next_word_flag.clear()
        self.root.update()

    def handle_keypress(self, event):
        if event.keysym == "Escape":
            self.stop_CD_flag.set()
            self.layout_end(self.root, -1)  # End game
            return

        current_word = self.words_to_type[self.current_word_index]

        if event.char == current_word[len(self.keys_pressed)]:
            self.keys_pressed += event.char
            tk_layout.update_text(self.root, self.GE[3], current_word, len(self.keys_pressed))
            self.root.update()

            if self.keys_pressed == current_word:  # Word completed
                self.stop_CD_flag.set()  # Stop the current countdown
                self.prepare_next_word()

    def prepare_next_word(self):
        self.current_word_index += 1
        self.keys_pressed = ""

        if self.cLife == 0:
            self.layout_end(self.root, -100)  # End game
        elif self.current_word_index < len(self.words_to_type):
            self.update_game_ui()  # Show next word
            self.restart_CD_flag.set()
            self.remaining_time = DEFAULT_TIME  # Reset timer
        else:
            self.layout_end(self.root, self.totalTime)  # End game



