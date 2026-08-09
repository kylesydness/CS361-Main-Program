import zmq

# Connect to cryptogram maker:
context = zmq.Context()
CM = context.socket(zmq.REQ)
CM.connect("tcp://localhost:4454")

def cryptofy(input):
    CM.send_string(str(input))
    output = CM.recv()
    return output.decode()

class Beat:
    def __init__(self, text: str, choices: list, recaps: list, children: list, status: bool = True):
        self.text = text           #text to be printed for player
        self.choices = choices     #options for player to select from
        self.recaps = recaps
        self.children = children   #next beat based on children
        self.status = status       #if true, game is still active, if false, game over

#ENDINGS:
# From b1
e1 = Beat("You keep walking and continue your day like normal.", [], [], ["good"], False)

# OTHER BEATS:
# From b2:
b3 = Beat("You bring the chain around your neck and clasp the Necklace. A chill goes down your spine. "
            "\"$NAME$,\" you hear someone call out in the distance behind you. You turn around, but you're alone."
            " Strange. Maybe it's time you head home.\n\n"
            "Today seems like one of those off days. On the walk home, you can't shake this feeling that someone is "
            "following you. You even feel a hand on your shoulder once in a while. You nearly trip several times for no "
            "apparent reason. What a klutz! Maybe you're just tired. Bed is sounding better and better by the minute.\n\n"
            "By the time you get home, the weather has cooled off and the sun has set. It's unusually dark on your street. "
            "For some reason the street lights aren't on.\n\n"
            "You finally make it inside and get ready for bed. You reach behind your neck to take off the necklace, "
            "but can't find the clasp...",
            ["Keep trying to\ntake it off", "Stop trying to\ntake it off"],
            ["\nYou tried to take the Necklace off", "\nYou didn't try to take the Necklace off"], [0,0])

b4 = Beat("You put the Necklace in your pocket. Who knows where that thing has been.\n\n"
            "You continue the rest of your walk. You notice the weather cooling off, and sunset feels like it comes sooner than usual."
            "You keep getting the feeling like someone's watching you, but you don't know why."
            " Several times, you look over your shoulder, but never see anyone out of the ordinary.\n\n"
            "It feels like a big relief when you get home. You take the Necklace out of your pocket and stare at it for a moment."
            " Something about it is just so alluring. You look at the indecipherable writing on the horseshoe in the bird's talons: "
            f"{cryptofy('"servant of raum"')}. What language could that be? What alphabet? And why does it look so similar to "
            "the english alphabet, yet weirdly off?\n\n You check the time and realize you should get to bed soon. But you "
            "look back at the Necklace, curious...",
            ["Bedtime, look into\nthe Necklace tomorrow", "Research the\nnecklace now"],
            ["\nYou went to bed right after getting home", "\nYou stayed up to research the necklace"],
            [0,0])

# From b1:
b2 = Beat("You pick up the necklace. It's heavier than you expected. Upon closer inspection, the bird looks like a "
            "raven, or maybe a crow? Its wings are spread and in its talons is a horseshoe with some tiny engraving "
            "along it. It's definitely not English, but the characters almost look like normal letters: "
            f"{cryptofy('"servant of raum"')}. But it's definitely some other alphabet...",
            ["Put the\nNecklace on", "Put the Necklace\nin your pocket"],
            ["\nYou put the Necklace on", "\nYou put the necklace in your pocket"], [b3, b4])

#Start:
b1 = Beat("$NAME$, you are walking through a park one afternoon. The weather is warm, the sun is out, and the grass is "
            "green. Something shiny catches the corner of your eye. You look over and see a silver object in the grass nearby."
            " You walk toward it to see it’s a chain necklace with some sort of bird as the pendant. You’re not quite sure why, "
            "but something about the necklace seems to be attracting you toward it, as if it’s calling out to you in somehow…",
            ["Pick up the\nNecklace", "Leave the Necklace\nwhere it is"],
            ["You picked up the Necklace", "You left the Necklace on the ground"],
            [b2, e1])
