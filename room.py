import random


class Room:
    def __init__(self, name, items=None, connecting_rooms=None):
        if items is None:
            items = []
        if connecting_rooms is None:
            connecting_rooms = {
                "North": None,
                "South": None,
                "East": None,
                "West": None
            }
        self.name = name
        self.items = items
        self.connecting_rooms = connecting_rooms


def random_between_one_five():  # random number from 1 to 5
    return random.randrange(1, 6, 1)


# state["rooms"] data structure = [
#   {
#       name: "",
#       items: [
#           {
#               name: count
#            }
#       ],
#       connecting_rooms: [
#           {
#               direction: room_name
#           }
#       ]
#   }
def create_rooms(rooms):  # create base state for rooms
    storage = []
    for room, attributes in rooms.items():
        current_room = Room(room, attributes["items"], attributes["Navigation"])
        storage.append(current_room)

    return storage


room_attributes = {
    "Library": {
        "items": [
            {"Granny's Ancient Cookbook": 1}
        ],
        "Navigation": {
            "North": None,
            "South": "Hallway 1",
            "East": "Cellar",
            "West": None
        }
    },
    "Cellar": {
        "items": [
            {"Cake Tin": random_between_one_five()},
        ],
        "Navigation": {
            "North": None,
            "South": "Study",
            "East": None,
            "West": "Library"
        }
    },
    "Hallway 1": {
        "items": [],
        "Navigation": {
            "North": "Library",
            "South": "Entryway",
            "East": "Study",
            "West": None
        }
    },
    "Study": {
        "items": [
            {"Strong Brewed Coffee": random_between_one_five()}
        ],
        "Navigation": {
            "North": "Cellar",
            "South": None,
            "East": None,
            "West": "Hallway 1"
        }
    },
    "Dining Room": {
        "items": [],
        "Navigation": {
            "North": None,
            "South": "Kitchen",
            "East": None,
            "West": None
        }
    },
    "Bedroom": {
        "items": [
            {"Cocoa Powder": random_between_one_five()}
        ],
        "Navigation": {
            "North": None,
            "South": "Hallway 2",
            "East": None,
            "West": None
        }
    },
    "Entryway": {
        "items": [],
        "Navigation": {
            "North": "Hallway 1",
            "South": "Yard",
            "East": "Kitchen",
            "West": None
        }
    },
    "Kitchen": {
        "items": [
            {"Sugar": random_between_one_five()},
            {"Milk": random_between_one_five()},
            {"Mascarpone Cheese": random_between_one_five()},
            {"Vanilla Extract": random_between_one_five()}
        ],
        "Navigation": {
            "North": "Dining Room",
            "South": "Pantry",
            "East": "Hallway 2",
            "West": "Entryway"
        }
    },
    "Hallway 2": {
        "items": [],
        "Navigation": {
            "North": "Bedroom",
            "South": None,
            "East": None,
            "West": "Kitchen"
        }
    },
    "Granny's Flat": {
        "items": [
            {"Rum": random_between_one_five()}
        ],
        "Navigation": {
            "North": None,
            "South": None,
            "East": "Yard",
            "West": None
        }
    },
    "Yard": {
        "items": [
            {"Egg": random_between_one_five()}
        ],
        "Navigation": {
            "North": "Entryway",
            "South": None,
            "East": None,
            "West": "Granny's Flat"
        }
    },
    "Pantry": {
        "items": [
            {"Egg": 1},
            {"Ladyfinger Cookie": random_between_one_five()},
            {"Sugar": random_between_one_five()}
        ],
        "Navigation": {
            "North": "Kitchen",
            "South": None,
            "East": None,
            "West": None
        }
    }
}
