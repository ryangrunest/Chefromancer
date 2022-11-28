from random import randrange
import time


def get_new_location(state):
    state["chefromancer_location"] = state["rooms"][randrange(0, len(state["rooms"]), 1)].name


def get_new_player_location(state):
    state["player_location"] = state["rooms"][randrange(0, len(state["rooms"]), 1)].name


def display_caught_by_chefromancer(state):
    print("You walk into the room and run into the Chefromancer!")
    print("You feel a swift knock in the head, and everything goes dark...")
    time.sleep(1)
    print("You eventually wake up, finding yourself in a weird location...")
    time.sleep(1)
    print("Checking your backpack, all your items are gone.")
    print("The Chefromancer must have taken them!")
    # remove items in inventory
    state["player_items"] = {}
    # update player location
    get_new_player_location(state)
    # update chefromancer location
    get_new_location(state)
    time.sleep(2)
    return


def check_chefromancer_roll(state):
    print("Chefromancer location: {}, player location: {}".format(state["chefromancer_location"], state["player_location"]))
    if state["chefromancer_location"] == state["player_location"]:
        # oh, no!
        return True
    else:
        return False
