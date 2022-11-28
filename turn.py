import time
from consolemenu import *
from consolemenu.items import *
import chefromancer


def update_player_location(state, room_index):
    # update player location
    directions = ["North", "South", "East", "West"]
    count = 0
    for room in state["rooms"]:
        if room.name == state["player_location"]:
            for direction in directions:
                if room.connecting_rooms[direction] is not None:
                    if count == room_index:
                        state["player_location"] = room.connecting_rooms[direction]

                    count += 1
    # update chefromancer location
    chefromancer.get_new_location(state)
    # display new turn
    return turn(state)


def select_item(state, item_index):
    for room in state["rooms"]:
        if room.name == state["player_location"]:
            room.items[item_index]
            for name, count in room.items[item_index].items():
                # add to inventory
                if name in state["player_items"]:
                    state["player_items"][name] += 1
                else:
                    state["player_items"][name] = 1

                # remove item from room
                room.items[item_index][name] -= 1
                print('You picked up a {}!'.format(name))
                time.sleep(2)

                # go to main turn
                return turn(state)


def display_new_room_menu(state):
    strings = ["Search for items", "Move to an adjacent room", "Check your backpack"]
    title = 'You find yourself in the {}.'.format(state["player_location"])
    sub_title = "What would you like to do?"
    display_new_room_menu_selection = SelectionMenu.get_selection(strings, title, sub_title, show_exit_option=False)
    return display_new_room_menu_selection


def display_select_items_menu(state):
    strings = []
    title = "After searching for a bit, you find the following items..."
    sub_title = "Select an item or go back."

    for room in state["rooms"]:
        if room.name == state["player_location"]:
            for item in room.items:
                for name, count in item.items():
                    if count >= 1:
                        strings.append("{}: (x{})".format(name, count))

    if len(strings) < 1:
        print('After searching for a bit, you don\'t find anything interesting.')
        time.sleep(2)
        return turn(state)
    else:
        strings.append("Go back")
        display_select_items_menu_selection = SelectionMenu.get_selection(strings, title, sub_title, show_exit_option=False)

        if display_select_items_menu_selection + 1 == len(strings):  # user selected go back
            return turn(state)
        else:
            return select_item(state, display_select_items_menu_selection)


def display_room_move_menu(state):
    strings = []
    title = "Which direction would you like to go?"
    directions = ["North", "South", "East", "West"]

    for room in state["rooms"]:
        if room.name == state["player_location"]:
            for direction in directions:
                if room.connecting_rooms[direction] is not None:
                    strings.append("{} to {}".format(direction, room.connecting_rooms[direction]))

    display_room_move_menu_selection = SelectionMenu.get_selection(strings, title, show_exit_option=False)
    return update_player_location(state, display_room_move_menu_selection)


def display_player_items(state):
    print("These are the current items in your inventory:")
    for item, count in state["player_items"].items():
        print("{} x{}".format(item, count))
    time.sleep(2)
    return turn(state)


def turn(state):
    # check if chefromancer is in your room
    chefromancer_is_in_the_room = chefromancer.check_chefromancer_roll(state)
    if chefromancer_is_in_the_room:
        chefromancer.display_caught_by_chefromancer(state)
        return turn(state)
    else:
        turn_selection = display_new_room_menu(state)

        if turn_selection == 0:  # search for items
            return display_select_items_menu(state)
        elif turn_selection == 1:  # move to an adjacent room
            return display_room_move_menu(state)
        elif turn_selection == 2:  # display item inventory
            return display_player_items(state)
