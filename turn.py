import time
from random import randrange
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


def select_item(state, item_name):
    item_index_in_room = 0
    for room in state["rooms"]:
        if room.name == state["player_location"]:
            for item in room.items:
                for name, count in item.items():
                    if name == item_name:
                        # remove item from room
                        room.items[item_index_in_room][name] -= 1
                        print('You picked up one {}.'.format(name))
                        time.sleep(2)

                        # add to inventory
                        if name in state["player_items"]:
                            state["player_items"][name] += 1
                        else:
                            state["player_items"][name] = 1

                        # go to main turn
                        return turn(state)

                item_index_in_room += 1


def display_new_room_menu(state):
    strings = []
    title = 'You find yourself in the {}.'.format(state["player_location"])
    sub_title = "What would you like to do?"

    if state["player_location"] == "Kitchen":
        strings = [
            "Search for items",
            "Move to an adjacent room",
            "Check your backpack",
            "Store all items from your backpack in the kitchen",
            "Bake Cake",
            "End Game"
        ]
    else:
        strings = ["Search for items", "Move to an adjacent room", "Check your backpack", "End Game"]

    display_new_room_menu_selection = SelectionMenu.get_selection(strings, title, sub_title, show_exit_option=False)
    return display_new_room_menu_selection


def display_select_items_menu(state):
    strings = []
    title = "After searching for a bit, you find the following items..."
    sub_title = "Select an item or go back."
    available_items = []

    for room in state["rooms"]:
        if room.name == state["player_location"]:
            for item in room.items:
                for name, count in item.items():
                    if count >= 1:
                        strings.append("{}: (x{})".format(name, count))
                        available_items.append(name)

    if len(strings) < 1:
        print('After searching for a bit, you don\'t find anything interesting.')
        time.sleep(2)
        return turn(state)
    else:
        strings.append("Go back")
        display_select_items_menu_selection = SelectionMenu.get_selection(strings, title, sub_title,
                                                                          show_exit_option=False)

        if display_select_items_menu_selection + 1 == len(strings):  # user selected go back
            return turn(state)
        else:
            return select_item(state, available_items[display_select_items_menu_selection])


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


def attempt_to_bake_cake(state):
    # it doesn't matter if there is more than one item, we just need one of each
    player_found_items = {**state["player_items"], **state["kitchen_stored_items"]}
    if len(player_found_items) > 11:  # total item count in game, player found all items
        # bake the cake
        print("You whip up the best tiramisu you've ever made.")
        time.sleep(2)
        print("Right as you finish, the chefromancer walks in.")
        time.sleep(2)
        print("He sees the delicious dessert you have made, and sheds a single tear.")
        print('"Golly gee, that is the best tiramisu I\'ve ever seen!", he says.')
        time.sleep(3)
        print("He sinks to the floor, defeated. "
              "In doing so a magical orb drops from his coat and shatters on the floor!")
        print("Suddenly a bright light flashes in the room!")
        time.sleep(2)
        print("When you open your eyes, where the chefromancer lay is now a pile of cocoa powder.")
        time.sleep(3)
        print("Congratulations, you won the game! You managed to win in {} turns.".format(state["turn_count"]))
        exit(200)
    else:
      print("Total items collected between kitchen and your backpack: {}. Total items in game: 11".format(
            len(player_found_items)))
      time.sleep(1)
      print("You don't have all of the required items yet!")
      time.sleep(3)
      turn(state)


def store_items_in_kitchen(state):
    for itemName, itemNumber in state["player_items"].items():
        if itemName not in state["kitchen_stored_items"]:
            state["kitchen_stored_items"][itemName] = itemNumber
        else:
            state["kitchen_stored_items"][itemName] += itemNumber
    state["player_items"] = {}
    print("One by one, you take all the items in your backpack and store them in hidden spots in the kitchen...")
    time.sleep(2)
    return turn(state)


def turn(state):
    state["turn_count"] += 1
    # check if chefromancer is in your room
    chefromancer_is_in_the_room = chefromancer.check_chefromancer_roll(state)
    if chefromancer_is_in_the_room:
        chefromancer.display_caught_by_chefromancer(state)
        # check if enough items in game
        if not chefromancer.enough_items_in_game(state):
            print("You ran out of enough items in the game to win.")
            print("The chefromancer has officially ruined your dinner party.")
            print("Please try again.")
            exit(200)
        return turn(state)
    else:
        turn_selection = display_new_room_menu(state)

        if state["player_location"] != "Kitchen":
            if turn_selection == 0:  # search for items
                return display_select_items_menu(state)
            elif turn_selection == 1:  # move to an adjacent room
                return display_room_move_menu(state)
            elif turn_selection == 2:  # display item inventory
                return display_player_items(state)
            elif turn_selection == 3:  # end game
                print("You lasted {} turns!".format(state["turn_count"]))
                print("Thank you for playing, I hope you had fun!")
                exit(200)
        else:
            if turn_selection == 0:  # search for items
                return display_select_items_menu(state)
            elif turn_selection == 1:  # move to an adjacent room
                return display_room_move_menu(state)
            elif turn_selection == 2:  # display item inventory
                return display_player_items(state)
            elif turn_selection == 3:  # store items in kitchen
                store_items_in_kitchen(state)
            elif turn_selection == 4:  # bake cake
                attempt_to_bake_cake(state)
            elif turn_selection == 5:  # end game
                print("You lasted {} turns!".format(state["turn_count"]))
                print("Thank you for playing, I hope you had fun!")
                exit(200)
