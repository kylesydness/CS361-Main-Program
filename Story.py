
class Beat:
    def __init__(self, text: str, choices: list, recaps: list, children: list, status: bool = True):
        self.text = text           #text to be printed for player
        self.choices = choices     #options for player to select from
        self.recaps = recaps
        self.children = children   #next beat based on children
        self.status = status       #if true, game is still active, if false, game over

e1 = Beat("You keep walking and continue your day like normal.", [], [], [], False)

b2 = Beat("You pick up the necklace. It's heavier than you expected. Upon closer inspection, the bird looks like a raven, or maybe a crow? Its wings are spread and in its talons is a horseshoe with some tiny engraving along it. It's definitely not English, so you can't makeout what it says.",
          ["Put the\nNecklace on", "Put the Necklace\nin your pocket"], ["You put the Necklace on", "You put the necklace in your pocket"], [0, 0])

b1 = Beat("$NAME$, you are walking through a park one afternoon. The weather is warm, the sun is out, and the grass is "
          "green. Something shiny catches the corner of your eye. You look over and see a silver object in the grass nearby. You walk toward it to see it’s a chain necklace with some sort of bird as the pendant. You’re not quite sure why, but something about the necklace seems to be attracting you toward it, as if it’s calling out to you in somehow…",
          ["Pick up the\nNecklace", "Leave the Necklace\nwhere it is"],
          ["You picked up the Necklace", "You left the Necklace on the ground"],
          [b2, e1])
