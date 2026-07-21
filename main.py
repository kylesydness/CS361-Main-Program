from tkmacosx import Button
import tkinter as tk
from tkinter import ttk, CENTER, BOTTOM, TOP

# Colors:
BG_COLOR = "#000000"
HEADER_COLOR = "#FF2600"
BUTTON_COLOR = "#941100"
SELECTED_COLOR = "#FF2600"
BODY_COLOR = "#FFFFFF"
SETTING_COLOR = "#111111"
SETTING_SEL = "#222222"

# Font styles:
HEADER_FONT = "Herculanum"
BODY_FONT = "Bodoni 72"

small_size = 20
medium_size = 25
large_size = 30

slow_speed = 50
medium_speed = 30
fast_speed = 10

FONT_SIZE = medium_size

FONT_SPEED = medium_speed


def change_size(new_size):
    global FONT_SIZE
    FONT_SIZE = new_size


def change_speed(new_speed):
    global FONT_SPEED
    FONT_SPEED = new_speed


class TkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("The Cryptic Necklace")
        self.geometry("1440x800")
        self.resizable(True, True)

        # Window/background
        # display area
        display = tk.Frame(self)
        display.pack(side="top", fill="both", expand=True)
        display.grid_rowconfigure(0, weight=1)
        display.grid_columnconfigure(0, weight=1)
        self.configure(background=BG_COLOR)

        self.frames = {}

        for S in (home_screen, tutor_screen, name_screen, text_screen, game_screen, recap_screen, over_screen):
            frame = S(display, self)
            self.frames[S] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(home_screen)

    def show_frame(self, name, last=None, l_name=None):
        frame = self.frames[name]
        if not last is None:
            frame.set_prev_screen(last, l_name)
        frame.tkraise()

class screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=BG_COLOR)

        # HEADER
        self.header = tk.Label(self, bg=BG_COLOR, fg=HEADER_COLOR, font=(HEADER_FONT, 60))

        #MAIN TEXT:
        self.string = "Placeholder"

        # DESCRIPTION
        self.description = tk.Label(self, bg=BG_COLOR, fg=BODY_COLOR, font=(BODY_FONT, FONT_SIZE), wraplength=1100, justify=tk.LEFT)

        # EXAMPLE CHOICES
        self.choice_1 = Button(self,
                               text="Example\nchoice 1",
                               fg=BODY_COLOR,
                               bd=5,
                               bg=BUTTON_COLOR,
                               activebackground=SELECTED_COLOR,
                               font=(BODY_FONT, FONT_SIZE),
                               highlightthickness=2,
                               padx=3, pady=3,
                               overrelief=tk.SUNKEN)

        self.choice_2 = Button(self,
                               text="Example\nchoice 2",
                               fg=BODY_COLOR,
                               bd=5,
                               bg=BUTTON_COLOR,
                               activebackground=SELECTED_COLOR,
                               font=(BODY_FONT, FONT_SIZE),
                               highlightthickness=2,
                               padx=3, pady=3,
                               overrelief=tk.SUNKEN)

        # Button images:
        back_img = tk.PhotoImage(file="Buttons/back_button.png").subsample(2,2)
        recap_img = tk.PhotoImage(file="Buttons/recap_button.png").subsample(2,2)
        text_img = tk.PhotoImage(file="Buttons/text_button.png").subsample(2,2)
        tutorial_img = tk.PhotoImage(file="Buttons/tutorial_button.png").subsample(2,2)

        # info for back button:
        self.prev_screen = None
        self.prev_name = None

        # OPTIONS
        # back
        self.back_button = Button(self,
                                  command=lambda: controller.show_frame(self.prev_screen),
                                  font=(BODY_FONT, FONT_SIZE - 5),
                                  image=back_img, compound=TOP,
                                  bg=SETTING_COLOR, fg=BODY_COLOR,
                                  activebackground=SETTING_SEL,
                                  highlightcolor=BODY_COLOR,
                                  overrelief=tk.SUNKEN,
                                  padx=0, pady=0)


        # recap
        self.recap = Button(self,
                            text="Recap",
                            image=recap_img, compound=TOP,
                            bg=SETTING_COLOR, fg=BODY_COLOR,
                            font=(BODY_FONT, FONT_SIZE - 5),
                            activebackground=SETTING_SEL,
                            highlightcolor=BODY_COLOR,
                            overrelief=tk.SUNKEN,
                            padx=0, pady=0)


        # text settings
        self.text_button = Button(self,
                                    text="Text Settings",
                                    font=(BODY_FONT,FONT_SIZE-5),
                                    image=text_img, compound=TOP,
                                    bg=SETTING_COLOR, fg=BODY_COLOR,
                                    activebackground=SETTING_SEL,
                                    highlightcolor=BODY_COLOR,
                                    overrelief=tk.SUNKEN,
                                    padx=0, pady=0)


        # tutorial
        self.tutorial_button = Button(self,
                                        text="How to Play",
                                        font=(BODY_FONT, FONT_SIZE - 5),
                                        image=tutorial_img, compound=TOP,
                                        bg=SETTING_COLOR, fg=BODY_COLOR,
                                        activebackground=SETTING_SEL,
                                        highlightcolor=BODY_COLOR,
                                        overrelief=tk.SUNKEN,
                                        padx=0, pady=0)

    # Placements:
        # TEXT:
        # self.header.place(relx=0.5, rely=0.05, anchor=tk.N)
        # self.description.place(relx=0.115, rely=0.2, anchor=tk.NW)
        #CHOICES:
        # self.choice_1.configure(text=choice_1)
        # self.choice_1.place(relx=0.45, rely=0.75, anchor=tk.E)
        # self.choice_2.configure(text=choice_2)
        # self.choice_2.place(relx=0.55, rely=0.75, anchor=tk.W)
        #NAVIGATION:
        # self.back_button.place(relx=0, rely=0, anchor=tk.NW)
        # self.recap.place(relx=0, rely=1, anchor=tk.SW)
        # self.text_button.place(relx=0.89, rely=0.82)
        # self.tutorial_button.place(relx=0.79, rely=0.82)

    def print_desc(self, char=1):
        self.description.config(text=self.string[:char])
        if char < len(self.string):
            root.after(FONT_SPEED, lambda: self.print_desc(char + 1))
        if char >= len(self.string):
            self.choice_2.place(relx=0.55, rely=0.75, anchor=tk.W)
            self.choice_1.place(relx=0.45, rely=0.75, anchor=tk.E)

    def set_prev_screen(self, prev_screen, prev_name):
        self.prev_screen = prev_screen
        self.prev_name = prev_name
        self.back_button.configure(text=f"Back to\n{self.prev_name}")
        self.print_desc()

class home_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # tk.Frame.__init__(self, parent)
        # HEADER
        self.header.config(text="The Cryptic\nNecklace", font=(HEADER_FONT, 80))
        self.header.place(relx=0.5, rely=0.3, anchor=CENTER)

        # DESCRIPTION
        self.description.config(text="Can you decypher what the necklace is before it's too late?")
        self.description.place(relx=0.5, rely=0.5, anchor=CENTER)

        # MAIN CHOICE:
        self.start_button = Button(self,
                                 text="Start Game", command=lambda: controller.show_frame(name_screen, home_screen, "Home"),
                                 fg=BODY_COLOR,
                                 bd=5,
                                 bg=BUTTON_COLOR,
                                 activebackground=SELECTED_COLOR,
                                 font=(BODY_FONT,FONT_SIZE),
                                 highlightthickness=2,
                                 padx=3, pady=3,
                                 overrelief=tk.SUNKEN)
        self.start_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        # OPTIONS
        #   tutorial
        self.tutorial_button.config(command=lambda: controller.show_frame(tutor_screen, home_screen, "Home"))
        self.tutorial_button.place(relx=0.79, rely=0.82)

        #   text settings
        self.text_button.config(command=lambda: controller.show_frame(text_screen, home_screen, "Home"))
        self.text_button.place(relx=0.89, rely=0.82)

class tutor_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

        # HEADER
        self.header.config(text="How to Play")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)

        # MAIN TEXT
        self.string = ("The Cryptic Necklace is a text-based horror game that gives you the chance to be a character in your own horror story.\n"
            "\nFor each story beat, text will be displayed, describing what is happening in the story. Using the button(s) below the displayed text, you can choose how to progress in the story. BEWARE! Once you make a decision, it cannot be undone, and it will affect what happens next.\n"
            "\nIf you are unhappy with your decisions, you can exit the game at any time using the “Back to Home” button in the top left corner, but BE WARNED: you will lose all progress you’ve made!\n"
            "\nUse the 'Recap' button* in the bottom left to see a summary of your previous choices. ")
        self.description.place(relx=0.115, rely=0.2, anchor=tk.NW)

        # EXAMPLE CHOICES
        self.choice_1.config(text="Example\nchoice 1")
        self.choice_2.config(text="Example\nchoice 2")

        # RECAP NOTE
        self.recap_note = tk.Label(self,
                                text="*The recap button on this page is display only, and is not clickable.",
                                bg=BG_COLOR, fg=BODY_COLOR,
                                font=(BODY_FONT, FONT_SIZE),
                                wraplength=1100, justify=tk.LEFT)
        self.recap_note.place(relx=0.1, rely=.95, anchor=tk.SW)
        #Navigation placement:
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)
        self.recap.place(relx=0, rely=1, anchor=tk.SW)

class name_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

class text_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

class game_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

class recap_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

class over_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #tk.Frame.__init__(self, parent)

root = TkinterApp()
root.minsize(720, 400)
root.mainloop()