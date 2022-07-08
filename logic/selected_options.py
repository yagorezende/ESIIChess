import enum

# NOTE - ex. to convert a enum member to str: member_name = Oponent.HUMAN.name
# NOTE - ex. to get the enum members as a list: members = list(Oponent)
# NOTE - ex. to get the enum members as a list of str: members = [member.name for member in Oponent]
# NOTE - compare enum members with `is`: member is Oponent.HUMAN


class Oponent(enum.Enum):
    HUMAN = enum.auto()
    IA = enum.auto()


class Color(enum.Enum):
    WHITE = enum.auto()
    BLACK = enum.auto()
    RANDOM = enum.auto()


class Difficulty(enum.Enum):
    EASY = enum.auto()
    MEDIUM = enum.auto()
    HARD = enum.auto()
