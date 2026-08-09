from tkinter import StringVar
from docutils.parsers.rst.directives.tables import align
from tkmacosx import Button
import tkinter as tk
import Story as Story
import zmq
import json
from pathlib import Path

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

slow_speed = 33
medium_speed = 15
fast_speed = 1

FONT_SIZE = medium_size

FONT_SPEED = medium_speed

# Name:
PLAYER = ""

def change_size(new_size):
    global FONT_SIZE
    FONT_SIZE = new_size

def change_speed(new_speed):
    global FONT_SPEED
    FONT_SPEED = new_speed


# MICROSERVICES:
context = zmq.Context()

# Random Name Generator:
RNG = context.socket(zmq.REQ)
RNG.connect("tcp://localhost:5555")

def get_r_name():
    RNG.send_string("RandomName")
    return RNG.recv().decode()

# Data Manager:
RECAP = context.socket(zmq.REQ)
RECAP.connect("tcp://localhost:54631")
step = 0
cwd = Path(__file__).resolve().parent

def set_step(data):
    global step
    request = {
        "command": "set",
        "data": {"recap": {step: data}},
        "cwd": str(cwd)
    }
    step += 1
    RECAP.send_json(request)
    response = RECAP.recv_string()
    return response

def get_recap():
    global step
    choices = ""
    request = {
        "command": "get",
        "data": ["recap"],
        "cwd": str(cwd)
    }
    RECAP.send_json(request)
    response = RECAP.recv_string()
    recap = json.loads(response)["recap"]
    if not recap is None:
        for x in range(0, step):
            choices += recap[str(x)]
    else: choices = "Your choices will display here"
    return choices

def clear_recap():
    request = {
        "command": "set",
        "data": {"recap":None},
        "cwd": str(cwd)
    }
    global step
    step = 0
    RECAP.send_json(request)
    response = RECAP.recv_string()
    return response

# Timer:
TMR = context.socket(zmq.REQ)
TMR.connect("tcp://localhost:8463")

def timer(command):
    TMR.send_string(command)
    return TMR.recv_string()

# Reactive Phrases:
RP = context.socket(zmq.REQ)
RP.connect("tcp://localhost:6423")

def react(command):
    RP.send_string("reactphrase" + command)
    return RP.recv_string()

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
        self.config(background=BG_COLOR)

        self.frames = {}

        # create recap file
        clear_recap()

        for S in (home_screen, tutor_screen, name_screen, text_screen, game_screen, recap_screen, over_screen, confirmation_screen):
            frame = S(display, self)
            self.frames[S] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(home_screen)

    def show_frame(self, screen, last=None, l_name=None):
        frame = self.frames[screen]
        if not last is None:
            frame.set_screen(last, l_name)
        frame.tkraise()
        if screen == game_screen and last == home_screen and l_name == "Home":
            self.frames[game_screen].reset_game()

    def new_size(self, size):
        change_size(size)
        for frame in self.frames.values():
            frame.reconfigure()

    def end_game(self, ending, time):
        frame = self.frames[over_screen]
        frame.string = ending
        frame.time = time
        frame.reconfigure()
        frame.tkraise()
        frame.print_desc()


class screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=BG_COLOR)

        # HEADER
        self.header = tk.Label(self, bg=BG_COLOR, fg=HEADER_COLOR, font=(HEADER_FONT, round(FONT_SIZE*2.5)))

        #MAIN TEXT:
        self.string = "Placeholder"
        self.c1 = "choice 1"
        self.c2 = "choice 2"

        # DESCRIPTION
        self.description = tk.Label(self, text=self.string,
                                    bg=BG_COLOR, fg=BODY_COLOR,
                                    font=(BODY_FONT, FONT_SIZE),
                                    wraplength=1100, justify=tk.LEFT)

        # EXAMPLE CHOICES
        self.choice_1 = Button(self,
                               text=self.c1,
                               anchor=tk.CENTER,
                               fg=BODY_COLOR,
                               bd=6, justify=tk.CENTER,
                               bg=BUTTON_COLOR, bordercolor=BODY_COLOR,
                               activebackground=SELECTED_COLOR,
                               font=(BODY_FONT, FONT_SIZE),
                               highlightthickness=2,
                               padx=3, pady=3,
                               overrelief=tk.SUNKEN)

        self.choice_2 = Button(self,
                               text=self.c2,
                               anchor=tk.CENTER,
                               fg=BODY_COLOR,
                               bd=6, justify=tk.CENTER,
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
                                  image=back_img, compound=tk.TOP,
                                  bg=SETTING_COLOR, fg=BODY_COLOR,
                                  activebackground=SETTING_SEL,
                                  highlightcolor=BODY_COLOR,
                                  overrelief=tk.SUNKEN,
                                  padx=0, pady=0)

        # recap
        self.recap = Button(self,
                            text="Recap",
                            image=recap_img, compound=tk.TOP,
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
                                    image=text_img, compound=tk.TOP,
                                    bg=SETTING_COLOR, fg=BODY_COLOR,
                                    activebackground=SETTING_SEL,
                                    highlightcolor=BODY_COLOR,
                                    overrelief=tk.SUNKEN,
                                    padx=0, pady=0)


        # tutorial
        self.tutorial_button = Button(self,
                                        text="How to Play",
                                        font=(BODY_FONT, FONT_SIZE - 5),
                                        image=tutorial_img, compound=tk.TOP,
                                        bg=SETTING_COLOR, fg=BODY_COLOR,
                                        activebackground=SETTING_SEL,
                                        highlightcolor=BODY_COLOR,
                                        overrelief=tk.SUNKEN,
                                        padx=0, pady=0)

    def print_desc(self, char=1):
        self.description.config(text=self.string[:char])
        if char == 1:
            self.choice_1.place_forget()
            self.choice_2.place_forget()
        if char < len(self.string):
            root.after(FONT_SPEED, lambda: self.print_desc(char + 1))
        if char >= len(self.string):
            self.choice_1.config(text=self.c1, state=tk.NORMAL, anchor = tk.CENTER, justify = tk.CENTER)
            self.choice_2.config(text=self.c2, state=tk.NORMAL, anchor = tk.CENTER, justify = tk.CENTER)
            self.choice_2.place(relx=0.55, rely=0.95, anchor=tk.SW)
            self.choice_1.place(relx=0.45, rely=0.95, anchor=tk.SE)

    def set_screen(self, prev_screen=None, prev_name=None):
        self.prev_screen = prev_screen
        self.prev_name = prev_name
        self.back_button.config(text=f"Back to\n{self.prev_name}", anchor = tk.CENTER, justify = tk.CENTER)
        self.print_desc()
    
    def reconfigure(self):
        # TEXT:
        self.header.config(font=(HEADER_FONT, round(FONT_SIZE*2.5)))
        self.description.config(font=(BODY_FONT, FONT_SIZE))
        # CHOICES:
        self.choice_1.config(font=(BODY_FONT, FONT_SIZE), justify=tk.CENTER)
        self.choice_2.config(font=(BODY_FONT, FONT_SIZE), justify=tk.CENTER)
        # NAVIGATION:
        self.back_button.config(font=(BODY_FONT, FONT_SIZE - 5))
        self.recap.config(font=(BODY_FONT, FONT_SIZE - 5))
        self.text_button.config(font=(BODY_FONT, FONT_SIZE - 5))
        self.tutorial_button.config(font=(BODY_FONT, FONT_SIZE - 5))

class home_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # HEADER
        self.header.config(text="The Cryptic\nNecklace", font=(HEADER_FONT, 80))
        self.header.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # DESCRIPTION
        self.description.config(text="Can you decypher what the necklace is before it's too late?")
        self.description.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # MAIN CHOICE:
        self.choice_1.config(text="Start Game", command=lambda: controller.show_frame(name_screen, home_screen, "Home"), anchor=tk.CENTER, justify=tk.CENTER)
        self.choice_1.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

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

        # HEADER
        self.header.config(text="How to Play")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)

        # MAIN TEXT
        self.string = """The Cryptic Necklace is a text-based horror game that gives you the chance to be a character in your own horror story.\n
For each story beat, text will be displayed, describing what is happening in the story. Using the button(s) below the displayed text, you can choose how to progress in the story. BEWARE! Once you make a decision, it cannot be undone, and it will affect what happens next.\n
If you are unhappy with your decisions, you can exit the game at any time using the “Back to Home” button in the top left corner, but BE WARNED: you will lose all progress you’ve made!\n
Use the "Recap" button* in the bottom left to see a summary of your previous choices. """
        self.description.place(relx=0.115, rely=0.2, anchor=tk.NW)

        # EXAMPLE CHOICES
        self.c1 = "Example\nchoice 1"
        self.c2 = "Example\nchoice 2"

        # RECAP NOTE
        self.recap_note = tk.Label(self,
                                text="*The recap button on this page is display only, and is not clickable.",
                                bg=BG_COLOR, fg=BODY_COLOR,
                                font=(BODY_FONT, FONT_SIZE-5),
                                wraplength=1100, justify=tk.LEFT)
        self.recap_note.place(relx=0.1, rely=.99, anchor=tk.SW)
        #Navigation placement:
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)
        self.recap.place(relx=0, rely=1, anchor=tk.SW)

    def reconfigure(self):
        # TEXT:
        self.header.config(font=(HEADER_FONT, round(FONT_SIZE*2.5)))
        self.description.config(font=(BODY_FONT, FONT_SIZE))
        self.recap_note.config(font=(BODY_FONT, FONT_SIZE))
        # CHOICES:
        self.choice_1.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.choice_2.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        # NAVIGATION:
        self.back_button.config(font=(BODY_FONT, FONT_SIZE - 5), anchor = tk.CENTER, justify = tk.CENTER)
        self.recap.config(font=(BODY_FONT, FONT_SIZE - 5), anchor = tk.CENTER, justify = tk.CENTER)

class text_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.string = """This is an example of how fast the text will display. Select a different speed from the options below to determine your preferred display speed. """
        
        # SPEED SECTION:
        # TEXT:
        self.header.config(text="Text speed")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)
        self.description.place(relx=0.115, rely=0.22, anchor=tk.NW)
        # OPTIONS:
        self.slow_button = Button(self,text="Slow",
                                  command=lambda: self.print_desc(1, slow_speed),
                               fg=BODY_COLOR, bg=BUTTON_COLOR,
                               bd=6, justify=tk.CENTER,
                               activebackground=SELECTED_COLOR,
                               font=(BODY_FONT, FONT_SIZE),
                               highlightthickness=2,
                               padx=3, pady=3,
                               overrelief=tk.SUNKEN)
        self.slow_button.place(relx=0.4, rely=0.4, anchor=tk.NE)

        self.med_speed_button = Button(self, text="Medium",
                                       command=lambda: self.print_desc(1, medium_speed),
                                  fg=BODY_COLOR, bg=BUTTON_COLOR,
                                  bd=6, justify=tk.CENTER,
                                  activebackground=SELECTED_COLOR,
                                  font=(BODY_FONT, FONT_SIZE),
                                  highlightthickness=2,
                                  padx=3, pady=3,
                                  overrelief=tk.SUNKEN)
        self.med_speed_button.place(relx=0.5, rely=0.4, anchor=tk.N)

        self.fast_button = Button(self, text="Fast",
                                  command=lambda: self.print_desc(1, fast_speed),
                                  fg=BODY_COLOR, bg=BUTTON_COLOR,
                                  bd=6, justify=tk.CENTER,
                                  activebackground=SELECTED_COLOR,
                                  font=(BODY_FONT, FONT_SIZE),
                                  highlightthickness=2,
                                  padx=3, pady=3,
                                  overrelief=tk.SUNKEN)
        self.fast_button.place(relx=0.6, rely=0.4, anchor=tk.NW)

        #SIZE SECTION:
        #TEXT:
        self.header2 = tk.Label(self,
                                text="Text Size",
                                bg=BG_COLOR, fg=HEADER_COLOR,
                                font=(HEADER_FONT, round(FONT_SIZE*2.5)))
        self.header2.place(relx=0.5, rely=0.6, anchor=tk.N)

        self.description2 = tk.Label(self,
                                     text = "Select your preferred text size below:",
                                     bg=BG_COLOR, fg=BODY_COLOR,
                                     font=(BODY_FONT, FONT_SIZE),
                                     wraplength=1100, justify=tk.LEFT)
        self.description2.place(relx=0.115, rely=0.75, anchor=tk.NW)
        # OPTIONS:
        self.small_button = Button(self, text="Small",
                                    command=lambda: self.resize(small_size),
                                    fg=BODY_COLOR, bg=BUTTON_COLOR,
                                    bd=6, justify=tk.CENTER, anchor=tk.CENTER,
                                    activebackground=SELECTED_COLOR,
                                    font=(BODY_FONT, small_size),
                                    highlightthickness=2,
                                    padx=3,
                                    overrelief=tk.SUNKEN)
        self.small_button.place(relx=0.4, rely=0.9, anchor=tk.E)

        self.med_size_button = Button(self, text="Medium",
                                        command=lambda: self.resize(medium_size),
                                        fg=BODY_COLOR, bg=BUTTON_COLOR,
                                        bd=6, justify=tk.CENTER, anchor=tk.CENTER,
                                        activebackground=SELECTED_COLOR,
                                        font=(BODY_FONT, medium_size),
                                        highlightthickness=2,
                                        padx=3,
                                        overrelief=tk.SUNKEN)
        self.med_size_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.large_button = Button(self, text="Large",
                                    command=lambda: self.resize(large_size),
                                    fg=BODY_COLOR, bg=BUTTON_COLOR,
                                    bd=6, justify = tk.CENTER, anchor=tk.CENTER,
                                    activebackground=SELECTED_COLOR,
                                    font=(BODY_FONT, large_size),
                                    highlightthickness=2,
                                    padx=3,
                                    overrelief=tk.SUNKEN)
        self.large_button.place(relx=0.6, rely=0.9, anchor=tk.W)

        # NAVIGATION:
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)

    def print_desc(self, char: int = 1, font_speed=None):
        #if char == 1:
            #self.reconfigure()
        if not font_speed is None:
            change_speed(font_speed)
        self.description.config(text=self.string[:char])
        if char < len(self.string):
            root.after(FONT_SPEED, lambda: self.print_desc(char + 1))

    def resize(self, size):
        if size != FONT_SIZE:
            root.new_size(size)

    def reconfigure(self):
        self.header.config(font=(HEADER_FONT, round(FONT_SIZE * 2.5)))
        self.header2.config(font=(HEADER_FONT, round(FONT_SIZE * 2.5)))

        self.description.config(font=(BODY_FONT, FONT_SIZE))
        self.description2.config(font=(BODY_FONT, FONT_SIZE))

        self.slow_button.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.med_speed_button.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.fast_button.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)

        self.back_button.config(font=(BODY_FONT, FONT_SIZE - 5))

class name_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.header.config(text="The Cryptic\nNecklace")

        self.string = "Enter your name below: "

        self.p_name = StringVar()
        global PLAYER
        if len(PLAYER) > 0:
            self.p_name.set(PLAYER)

        self.name_entry = tk.Entry(self, width=40, text=self.p_name, font=(BODY_FONT, FONT_SIZE))
        self.name_entry.place(relx=.5, rely=.52, anchor=tk.CENTER)

        # Placements:
        # TEXT:
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)
        self.description.config(anchor=tk.CENTER)
        self.description.place(relx=0.5, rely=0.38, anchor=tk.N)
        # NAME SUBMIT:
        self.choice_1.config(text="Begin", command=lambda: self.new_game(), anchor = tk.CENTER, justify = tk.CENTER)
        # RANDOM OPTION:
        self.choice_2.config(text="Random Name", command=lambda: self.random_name(),
                             font=(BODY_FONT, FONT_SIZE-5),
                             padx=0, pady=0)
        # NAVIGATION:
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)

        #   tutorial
        self.tutorial_button.config(command=lambda: controller.show_frame(tutor_screen, name_screen, "Game"))
        self.tutorial_button.place(relx=0.79, rely=0.82)

        #   text settings
        self.text_button.config(command=lambda: controller.show_frame(text_screen, name_screen, "Game"))
        self.text_button.place(relx=0.89, rely=0.82)

    def print_desc(self, char=1):
        self.description.config(text=self.string[:char])
        if char ==1:
            self.choice_1.place_forget()
            self.choice_2.place_forget()
        if char < len(self.string):
            root.after(FONT_SPEED, lambda: self.print_desc(char + 1))
        if char >= len(self.string):
            self.choice_1.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
            self.choice_2.place(relx=0.7, rely=0.52, anchor=tk.W)

    def new_game(self):
        global PLAYER
        PLAYER = self.p_name.get()
        if len(PLAYER) > 0:
            root.show_frame(game_screen, home_screen, "Home")

    def reconfigure(self):
        self.header.config(font=(HEADER_FONT, round(FONT_SIZE * 2.5)))
        self.name_entry.config(font=(BODY_FONT, FONT_SIZE))
        self.description.config(font=(BODY_FONT, FONT_SIZE))
        self.choice_1.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.choice_2.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.back_button.config(font=(BODY_FONT, FONT_SIZE-5))
        self.text_button.config(font=(BODY_FONT, FONT_SIZE-5))
        self.tutorial_button.config(font=(BODY_FONT, FONT_SIZE-5))

    def random_name(self):
        name = get_r_name()
        name = name.replace("\n", "")
        self.p_name.set(name)

class game_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # HEADER
        self.header.config(text="The Cryptic\nNecklace")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)

        self.beat = Story.b1

        # MAIN TEXT
        self.string = self.beat.text # to be replaced with first story beat info
        self.description.place(relx=0.115, rely=0.25, anchor=tk.NW)

        # CHOICES
        self.c1 = self.beat.choices[0]
        self.c2 = self.beat.choices[1]
        self.choice_1.config(command=lambda: self.new_beat(0), anchor = tk.CENTER, justify = tk.CENTER)
        self.choice_2.config(command=lambda: self.new_beat(1), anchor = tk.CENTER, justify = tk.CENTER)

        # OPTIONS
        # back to home
        self.back_button.config(text="Exit Game", command=lambda: self.exit_game())
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)

        #   tutorial
        self.tutorial_button.config(command=lambda: controller.show_frame(tutor_screen, game_screen, "Game"))
        self.tutorial_button.place(relx=0.79, rely=0.82)

        #   text settings
        self.text_button.config(command=lambda: controller.show_frame(text_screen, game_screen, "Game"))
        self.text_button.place(relx=0.89, rely=0.82)

        # recap option
        self.recap.config(command=lambda: controller.show_frame(recap_screen, game_screen, "Game"))
        self.recap.place(relx=.01, rely=0.82)

    def new_beat(self, selection):

        # microservice to save recap info
        set_step(self.beat.recaps[selection])

        # select next beat
        self.beat = self.beat.children[selection]
        self.string = self.beat.text.replace("$NAME$", PLAYER)

        # if game status is over, run game over function
        if self.beat.status is False:
            self.game_over()

        else:
            self.c1 = self.beat.choices[0]
            self.c2 = self.beat.choices[1]
            self.description.config(text=self.string.replace("$NAME$", PLAYER))
            self.choice_1.config(text=self.c1, anchor = tk.CENTER, justify = tk.CENTER)
            self.choice_2.config(text=self.c2, anchor = tk.CENTER, justify = tk.CENTER)
            self.print_desc()

    def game_over(self):
        if timer("timeractive") == "True":
            timer("timerstsp")
        game_time = timer("timer read")
        timer("timer reset")
        reaction = react(self.beat.children[0])
        root.end_game(reaction + "!\n" + self.string, game_time)

    def exit_game(self):
        #Add warning for game reset
        root.show_frame(confirmation_screen)

    def reset_game(self):
        self.beat = Story.b1
        self.string = self.beat.text.replace("$NAME$", PLAYER)
        self.c1 = self.beat.choices[0]
        self.c2 = self.beat.choices[1]
        self.reconfigure()
        clear_recap()
        #start/reset timer:
        if timer("timeractive") == "True":
            timer("timerstsp")
        timer("timerreset")
        timer("timerstsp")

class recap_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.string = get_recap()

        self.header.config(text="Your Choices")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)

        self.description.place(relx=0.115, rely=0.2, anchor=tk.NW)

    def set_screen(self, prev_screen=None, prev_name=None):
        self.prev_screen = prev_screen
        self.prev_name = prev_name
        self.back_button.config(text=f"Back to\nGame")
        self.description.config(text=get_recap())

class over_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # HEADER
        self.header.config(text="The Cryptic\nNecklace")
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)

        # PARTING WORDS
        self.description.place(relx=0.5, rely=0.3, anchor=tk.N)

        # TIME RESULTS
        self.time = 0
        self.show_time = tk.Label(self, text=f"Time to complete the game: {self.time}",
                                    bg=BG_COLOR, fg=BODY_COLOR,
                                    font=(BODY_FONT, FONT_SIZE),
                                    wraplength=1100, justify=tk.CENTER)

        # GAME OVER:
        self.header2 = tk.Label(self,
                                text="Game over",
                                bg=BG_COLOR, fg=HEADER_COLOR,
                                font=(HEADER_FONT, round(FONT_SIZE * 2.5)))

        # OPTIONS:
        self.recap = Button(self, text="Full Recap",
                                   command=lambda: controller.show_frame(recap_screen, over_screen, "Game"),
                                   fg=BODY_COLOR, bg=BUTTON_COLOR,
                                   bd=6, justify=tk.CENTER,
                                   activebackground=SELECTED_COLOR,
                                   font=(BODY_FONT, small_size),
                                   highlightthickness=2,
                                   padx=3, pady=3,
                                   overrelief=tk.SUNKEN)

        self.replay = Button(self, text="Play Again",
                                      command=lambda: controller.show_frame(name_screen, home_screen, "Home"),
                                      fg=BODY_COLOR, bg=BUTTON_COLOR,
                                      bd=6, justify=tk.CENTER,
                                      activebackground=SELECTED_COLOR,
                                      font=(BODY_FONT, medium_size),
                                      highlightthickness=2,
                                      padx=3, pady=3,
                                      overrelief=tk.SUNKEN)

        self.home = Button(self, text="Home",
                                   command=lambda: controller.show_frame(home_screen),
                                   fg=BODY_COLOR, bg=BUTTON_COLOR,
                                   bd=6, anchor=tk.CENTER,
                                   activebackground=SELECTED_COLOR,
                                   font=(BODY_FONT, large_size),
                                   highlightthickness=2,
                                   padx=3, pady=3,
                                   overrelief=tk.SUNKEN)

        #   tutorial
        self.tutorial_button.config(command=lambda: controller.show_frame(tutor_screen, over_screen, "Game"))
        self.tutorial_button.place(relx=0.79, rely=0.82)

        #   text settings
        self.text_button.config(command=lambda: controller.show_frame(text_screen, over_screen, "Game"))
        self.text_button.place(relx=0.89, rely=0.82)

    def reconfigure(self):
        self.header.config(font=(HEADER_FONT, round(FONT_SIZE * 2.5)))
        self.header2.config(font=(HEADER_FONT, round(FONT_SIZE * 2.5)))
        self.description.config(font=(BODY_FONT, FONT_SIZE), text=self.string, anchor = tk.N, justify=tk.CENTER)
        self.show_time.config(font=(BODY_FONT, FONT_SIZE), text=f"Time to complete the game: {self.time}")
        self.recap.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.replay.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)
        self.home.config(font=(BODY_FONT, FONT_SIZE), anchor = tk.CENTER, justify = tk.CENTER)

    def print_desc(self, char=1):
        self.description.config(text=self.string[:char])
        if char ==1:
            self.header2.place_forget()
            self.show_time.place_forget()
            self.recap.place_forget()
            self.replay.place_forget()
            self.home.place_forget()
        if char < len(self.string):
            root.after(FONT_SPEED, lambda: self.print_desc(char + 1))
        if char >= len(self.string):
            self.header2.place(relx=0.5, rely=0.45, anchor=tk.N)
            self.show_time.place(relx=0.5, rely=0.6, anchor=tk.N)
            self.recap.place(relx=0.4, rely=0.75, anchor=tk.E)
            self.replay.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
            self.home.place(relx=0.6, rely=0.75, anchor=tk.W)

    def ending(self, end):
        self.string = end

class confirmation_screen(screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.configure(background=SETTING_COLOR)

        self.header.config(text="The Cryptic\nNecklace", bg=SETTING_COLOR)
        self.header.place(relx=0.5, rely=0.05, anchor=tk.N)

        self.description.config(text="Are you sure?\n\nALL PROGRESS WILL BE LOST.",
                                bg=SETTING_COLOR, anchor=tk.N,
                                justify=tk.CENTER)
        self.description.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.choice_1.config(command=lambda: controller.show_frame(home_screen), text="Yes, go\nHome", anchor = tk.CENTER, justify = tk.CENTER)
        self.choice_2.config(command=lambda: controller.show_frame(game_screen), text="No, back\nto Game", anchor = tk.CENTER, justify = tk.CENTER)

        self.choice_1.place(relx=0.45, rely=0.6, anchor=tk.NE)
        self.choice_2.place(relx=0.55, rely=0.6, anchor=tk.NW)


root = TkinterApp()
root.minsize(720, 400)
root.mainloop()