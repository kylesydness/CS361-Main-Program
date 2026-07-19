from typing import Type

class Beat:
    def __init__(self, text: str, choices: list, children: list, parent = None, status: bool = True):
        self._text = text           #text to be printed for player
        self._choices = choices     #options for player to select from
        self._children = children   #next beat based on children
        self._parent = parent       #previous beat
        self._status = status       #if true, game is still active, if false, game over

    def __str__(self):
        return self._text

    def get_choices(self):
        return self._choices

    def get_status(self):
        return self._status

class choice:
    def __init__(self, text: str, recap: str):
        self.text = text
        self.recap = recap

