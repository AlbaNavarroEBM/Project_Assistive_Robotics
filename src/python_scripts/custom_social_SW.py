import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/GoodBoy.rdk" ### MODIFIQUEM EL NOM AFEGINT "Trial_"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink(args=absolute_path)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item("Hand")
Init_target = RDK.Item("Init")
Give_paw_app = RDK.Item("Give_paw_approach")
Give_paw = RDK.Item("Give_paw") 
Good_boy_app = RDK.Item("Good_boy_approach") 
Good_boy_1 = RDK.Item("Good_boy_1")
Good_boy_2 = RDK.Item("Good_boy_2")
Good_boy_3 = RDK.Item("Good_boy_3") 

# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Move to initial position
def move_to_init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

# Perform handshake sequence
### CANVIEM "hand shake" PER "Cane delivering"
def movement_1():
    print("Give me paw")
    robot.MoveL(Give_paw_app, True)
    robot.MoveL(Give_paw, True)
    robot.MoveL(Give_paw_app, True)
    print("Give me paw FINISHED")

# Perform "Give me 5" sequence
### CANVIEM "Give me 5" PER "Helping to get up"
def movement_2():
    print("Who is a good boy?!")
    robot.MoveL(Good_boy_app, True)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_2, True)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_3, True)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_app, True)
    print("Good boy FINISHED")

# Main sequence
def main():
    move_to_init()
    movement_1()
    movement_2()
    move_to_init()

# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Run main and handle closing
if __name__ == "__main__":
    main()
    confirm_close()
