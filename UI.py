from tkmacosx import Button
import tkinter as tk
from tkinter import ttk, CENTER


# Colors:
bg_color = "#000000"
header_color = "#FF2600"
button_color = "#941100"
selected_color = "#FF2600"
body_color = "#FFFFFF"

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

        self.screens = {}

        for S in (home_screen, tutor_screen, name_screen, text_screen, game_screen, recap_screen, over_screen):
            screen = S(display, self)
            self.screens[S] = screen
            screen.grid(row=0, column=0, sticky="nsew")
        self.show_screen(home_screen)

    def show_screen(self, name):
        screen = self.screens[name]
        screen.tkraise()

class home_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background=bg_color)
        # Header
        header = tk.Label(self, text="The Cryptic\nNecklace", bg=bg_color, fg=header_color, font=(header_font, 80))
        header.place(relx=0.5, rely=0.3, anchor=CENTER)

        # description
        description = tk.Label(self, text="Can you decypher what the necklace is before it's too late?", bg=bg_color, fg=body_color, font=(body_font, font_size))
        description.place(relx=0.5, rely=0.45, anchor=CENTER)

        # main choice:
        start_button = Button(self,
                                 text="Start Game", command=lambda: controller.show_screen(name_screen),
                                 fg=body_color,
                                 bd=5,
                                 bg=button_color,
                                 activebackground=selected_color,
                                 font=(body_font,font_size),
                                 highlightthickness=2,
                                 padx=3, pady=3,
                                 overrelief=tk.SUNKEN
                                 )
        start_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        # options
        #   tutorial
# INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.tutorial.place(relx=0.8, rely=0.95)
        #   text settigns
#INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settigns", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.t_settings.place(relx=0.9, rely=0.95)

class tutor_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        # back
# INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)
        # recap
# INSERT LOGO
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)

class name_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        # tutorial
        # INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.tutorial.place(relx=0.8, rely=0.95)
        # text settigns
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settigns", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.t_settings.place(relx=0.9, rely=0.95)
        # back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size))
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
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.tutorial.place(relx=0.8, rely=0.95)
        # text settigns
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settigns", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.t_settings.place(relx=0.9, rely=0.95)
        # back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)
        # recap
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)

class recap_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # options
        #   back
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color,
                             font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)

class over_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Main choices:

        # recap
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)
        # play again
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="recap", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)
        # back to home
        # INSERT LOGO/BUTTON
        self.back = tk.Label(self, text="Back to\n[remove from home]", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.back.place(relx=0, rely=0.1)

        # options
        #   tutorial
        # INSERT LOGO/BUTTON
        self.tutorial = tk.Label(self, text="How to Play", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.tutorial.place(relx=0.8, rely=0.95)
        #   text settigns
        # INSERT LOGO/BUTTON
        self.t_settings = tk.Label(self, text="Text Settigns", bg=bg_color, fg=body_color, font=(body_font, font_size))
        self.t_settings.place(relx=0.9, rely=0.95)


root = TkinterApp()
root.minsize(720, 400)
root.mainloop()