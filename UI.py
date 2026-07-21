from tkmacosx import Button
import tkinter as tk
from tkinter import ttk, CENTER, BOTTOM, TOP

# Colors:
bg_color = "#000000"
header_color = "#FF2600"
button_color = "#941100"
selected_color = "#FF2600"
body_color = "#FFFFFF"
setting_color = "#111111"
setting_sel = "#222222"

#Font styles:
header_font = "Herculanum"
body_font = "Bodoni 72"

small_size = 20
medium_size = 25
large_size = 30

font_size = medium_size

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
        self.configure(background=bg_color)

        self.frames = {}

        for S in (home_screen, tutor_screen, name_screen, text_screen, game_screen, recap_screen, over_screen):
            frame = S(display, self)
            self.frames[S] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(home_screen)


    def show_frame(self, name, last = None, l_name = None):
        frame = self.frames[name]
        if not last is None:
            frame.set_prev_screen(last, l_name)
        frame.tkraise()



class home_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_color)
        # HEADER
        header = tk.Label(self, text="The Cryptic\nNecklace", bg=bg_color, fg=header_color, font=(header_font, 80))
        header.place(relx=0.5, rely=0.3, anchor=CENTER)

        # DESCRIPTION
        description = tk.Label(self, text="Can you decypher what the necklace is before it's too late?", bg=bg_color, fg=body_color, font=(body_font, font_size))
        description.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Button images:
        back_img = tk.PhotoImage(file="Buttons/back_button.png").subsample(2,2)
        recap_img = tk.PhotoImage(file="Buttons/recap_button.png").subsample(2,2)
        text_img = tk.PhotoImage(file="Buttons/text_button.png").subsample(2,2)
        tutorial_img = tk.PhotoImage(file="Buttons/tutorial_button.png").subsample(2,2)

        # MAIN CHOICE:
        start_button = Button(self,
                                 text="Start Game", command=lambda: controller.show_frame(name_screen, home_screen,
                                                                                           "Home"),
                                 fg=body_color,
                                 bd=5,
                                 bg=button_color,
                                 activebackground=selected_color,
                                 font=(body_font,font_size),
                                 highlightthickness=2,
                                 padx=3, pady=3,
                                 overrelief=tk.SUNKEN)
        start_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        # OPTIONS
        #   tutorial
        tutorial_button = Button(self,
                                 text="How to Play",
                                 command=lambda: controller.show_frame(tutor_screen, home_screen, "Home"),
                                 image=tutorial_img,
                                 compound=TOP,
                                 bg=setting_color,
                                 fg=body_color,
                                 font=(body_font, font_size-5),
                                 activebackground=setting_sel,
                                 highlightcolor=body_color,
                                 overrelief=tk.SUNKEN,
                                 padx=0, pady=0)
        tutorial_button.place(relx=0.79, rely=0.82)

        #   text settings
        text_button = Button(self,
                                 text="Text Settings",
                                 command=lambda: controller.show_frame(text_screen, home_screen, "Home"),
                                 font=(body_font,font_size-5),
                                 image=text_img,
                                 compound=TOP,
                                 bg=setting_color,
                                 fg=body_color,
                                 activebackground=setting_sel,
                                 highlightcolor=body_color,
                                 overrelief=tk.SUNKEN,
                                 padx=0, pady=0)
        text_button.place(relx=0.89, rely=0.82)

class tutor_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_color)

        # HEADER
        header = tk.Label(self, text="How to Play", bg=bg_color, fg=header_color, font=(header_font, 60))
        header.place(relx=0.5, rely=0.05, anchor=tk.N)

        # DESCRIPTION
        description = tk.Label(self, text="The Cryptic Necklace is a text-based horror game that gives you the chance to be a character in your own horror story.\n\nFor each story beat, text will be displayed, describing what is happening in the story. Using the button(s) below the displayed text, you can choose how to progress in the story. BEWARE! Once you make a decision, it cannot be undone, and it will affect what happens next.\n\nIf you are unhappy with (your) decisions, you can exit the game at any time using the “Back to Home” button in the top right corner, but BE WARNED: you will lose all progress you’ve made!\n\nUse the 'Recap' button* in the bottom left to see a summary of your previous choices.", bg=bg_color,
                               fg=body_color, font=(body_font, font_size), wraplength=1100, justify=tk.LEFT)
        description.place(relx=0.5, rely=0.2, anchor=tk.N)

        # EXAMPLE CHOICES
        choice_1 = Button(self,
                              text="Example\nchoice 1",
                              fg=body_color,
                              bd=5,
                              bg=button_color,
                              activebackground=selected_color,
                              font=(body_font, font_size),
                              highlightthickness=2,
                              padx=3, pady=3,
                              overrelief=tk.SUNKEN)
        choice_1.place(relx=0.45, rely=0.75, anchor=tk.E)
        choice_2 = Button(self,
                          text="Example\nchoice 2",
                          fg=body_color,
                          bd=5,
                          bg=button_color,
                          activebackground=selected_color,
                          font=(body_font, font_size),
                          highlightthickness=2,
                          padx=3, pady=3,
                          overrelief=tk.SUNKEN)
        choice_2.place(relx=0.55, rely=0.75, anchor=tk.W)
        # RECAP NOTE
        recap_note = tk.Label(self,
                               text="*The recap button on this page is display only, and is not clickable.",
                               bg=bg_color,
                               fg=body_color, font=(body_font, font_size), wraplength=1100, justify=tk.LEFT)
        recap_note.place(relx=0.5, rely=.95, anchor=tk.S)
        # Button images:
        back_img = tk.PhotoImage(file="Buttons/back_button.png").subsample(2,2)
        recap_img = tk.PhotoImage(file="Buttons/recap_button.png").subsample(2,2)
        text_img = tk.PhotoImage(file="Buttons/text_button.png").subsample(2,2)
        tutorial_img = tk.PhotoImage(file="Buttons/tutorial_button.png").subsample(2,2)

        self.prev_screen = None
        self.prev_name = None

        # OPTIONS
        # back
        self.back_button = Button(self,
                                 text=f"Back to\n{self.prev_name}",
                                 command=lambda: controller.show_frame(self.prev_screen),
                                 font=(body_font, font_size - 5),
                                 image=back_img,
                                 compound=TOP,
                                 bg=setting_color,
                                 fg=body_color,
                                 activebackground=setting_sel,
                                 highlightcolor=body_color,
                                 overrelief=tk.SUNKEN,
                                 padx=0, pady=0)
        self.back_button.place(relx=0, rely=0, anchor=tk.NW)
        # example recap
        self.recap = Button(self,
                                 text="Recap",
                                 image=recap_img,
                                 compound=TOP,
                                 bg=setting_color,
                                 fg=body_color,
                                 font=(body_font, font_size-5),
                                 activebackground=setting_sel,
                                 highlightcolor=body_color,
                                 overrelief=tk.SUNKEN,
                                 padx=0, pady=0)
        self.recap.place(relx=0, rely=1, anchor=tk.SW)

    def set_prev_screen(self, prev_screen, prev_name):
        self.prev_screen = prev_screen
        self.prev_name = prev_name
        self.back_button.configure(text=f"Back to\n{self.prev_name}")

class name_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        # tutorial
        # INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.tutorial.place(relx=0.8, rely=0.95)
        # text settigns
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settings", bg=bg_color, fg=body_color, font=(body_font,
                                                                                                 font_size-5))
        self.t_settings.place(relx=0.9, rely=0.95)
        # back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)

class text_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        # back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)

class game_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        # tutorial
        # INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.tutorial.place(relx=0.8, rely=0.95)
        # text settings
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settings", bg=bg_color, fg=body_color, font=(body_font,
                                                                                                 font_size-5))
        self.t_settings.place(relx=0.9, rely=0.95)
        # back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)
        # recap
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)

class recap_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        #   back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)

class over_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Main choices:

        # recap
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)
        # play again
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.back.place(relx=0, rely=0.1)
        # back to home
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color, font=(body_font,
                                                                                                         font_size-5))
        self.back.place(relx=0, rely=0.1)

        # options
        #   tutorial
        # INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size-5))
        self.tutorial.place(relx=0.8, rely=0.95)
        #   text settigns
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settings", bg=bg_color, fg=body_color, font=(body_font,
                                                                                                 font_size-5))
        self.t_settings.place(relx=0.9, rely=0.95)

root = TkinterApp()
root.minsize(720, 400)
root.mainloop()