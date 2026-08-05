
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

slow_speed = 35
medium_speed = 20
fast_speed = 5

FONT_SIZE = medium_size

FONT_SPEED = medium_speed

PLAYER = ""

def change_size(new_size):
    global FONT_SIZE
    FONT_SIZE = new_size

def change_speed(new_speed):
    global FONT_SPEED
    FONT_SPEED = new_speed

def new_name(name):
    global PLAYER
    PLAYER = name

