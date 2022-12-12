# from random import randrange
from room import room_attributes, create_rooms
from turn import turn

# init base game state
state = {
    "chefromancer_location": "Dining Room",
    "player_location": "Entryway",
    "player_items": {},
    "kitchen_stored_items": {},
    "rooms": create_rooms(room_attributes),
    "turn_count": -1
}

turn(state)
