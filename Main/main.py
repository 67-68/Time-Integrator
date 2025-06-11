
import json
from CLI import mainMenu
from GUI import menuGUI

#Main function start
print("welcome to the time-integrater, it is a gadget that helps you to analyze your time distribusion")

#menu start
choice = input("CLI or GUI?just type the choice you want to")
if choice == "CLI":
    mainMenu()
else:
    menuGUI()
