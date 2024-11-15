from games import GameMenu
from players import PlayerMenu
from additional_functions import AdditionalFunctions

# Main menu
class MainMenu():
    options = ["Change to 'players' menu","Change to 'games' menu", "Additional functions", "Exit"]
    length = len(options)

    def players_menu():
        global menu_index
        menu_index = 1

    def games_menu():
        global menu_index
        menu_index = 2

    def additional_functions():
        global menu_index
        menu_index = 3

    functions = [players_menu, games_menu, additional_functions]

# Instances and list of menus
inst_MainMenu = MainMenu()
inst_PlayerMenu = PlayerMenu()
inst_GameMenu = GameMenu()
inst_AdditionalFunctions = AdditionalFunctions()

menus = [inst_MainMenu, inst_PlayerMenu, inst_GameMenu, inst_AdditionalFunctions]

# Globally defined values to keep a reference of
# current menu and selected option from it
menu_index = 0
option_index = 0

# Print menu and request input with error handling
def menu_input():
    for index in range(menus[menu_index].length):
        print(str(index + 1) + ". " + menus[menu_index].options[index])

    while True:
        try:
            input_value = int(input("Enter a value: "))
        except ValueError:
            print("Value must be an integer")
            continue

        if input_value > menus[menu_index].length or input_value < 1:
            print("Value out of range")
        else:
            break

    print("")
    return input_value

# Calls functions, changes menus or ends the script depending
# on the "menu_index" and "option_index" values.
while True:
    option_index = menu_input()

    if option_index == menus[menu_index].length and menu_index == 0:
        print("Program ended")
        break
    elif option_index == menus[menu_index].length and menu_index != 0:
        menu_index = 0
    else:
        menus[menu_index].functions[option_index - 1]()
        print("")