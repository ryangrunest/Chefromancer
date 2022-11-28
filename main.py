# from random import randrange
from room import room_attributes, create_rooms
import chefromancer
from turn import turn, display_select_items_menu

# init base game state
state = {
    "chefromancer_location": "Dining Room",
    "player_location": "Entryway",
    "player_items": {},
    "kitchen_stored_items": [],
    "rooms": create_rooms(room_attributes),
    "turn_count": 0
}
#
# for room in state["rooms"]:
#     print(room.name, room.items, room.connecting_rooms)

# print(state["chefromancer_location"])
# print(state["player_location"])

# chefromancer.get_new_location(state)
# print(state["chefromancer_location"])
turn(state)
# display_select_items_menu(state)
