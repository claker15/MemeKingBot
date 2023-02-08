from .wand import Wand

order = ["Wood", "Bone", "Steel", "Ivory"]


def create_wand(level):
    if level == "Wood":
        return Wand(10, 0, 3)
    elif level == "Bone":
        return Wand(15, 1, 4)
    elif level == "Steel":
        return Wand(20, 2, 5)
    elif level == "Ivory":
        return Wand(25, 3, 6)
    else:
        return Wand(10, 0, 3)


def upgrade_wand(level):
    new_index = order.index(level) + 1
    if new_index > len(order) - 1:
        return "Ivory"
    else:
        return order[new_index]


def downgrade_wand(level):
    new_index = order.index(level) - 1
    if new_index < 0:
        return "Wood"
    else:
        return order[new_index]
