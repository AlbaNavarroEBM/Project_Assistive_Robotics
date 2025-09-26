import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/Trial_Assistive_UR5e.rdk" ### MODIFIQUEM EL NOM AFEGINT "Trial_"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink(args=absolute_path)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item("Hand")
Init_target = RDK.Item("Init")
Movement_1_0 = RDK.Item("movement_1_0")
Movement_1_1 = RDK.Item("movement_1_1") ### MODIFIQUEM "App_shake" PER "movement_1_1"
Movement_1_2 = RDK.Item("movement_1_2") ### MODIFIQUEM "Shake" PER "movement_1_2"
Movement_1_3 = RDK.Item("movement_1_3")
Movement_1_4 = RDK.Item("movement_1_4")
Movement_2_1 = RDK.Item("movement_2_1") ### MODIFIQUEM "App_give5" PER "movement_2_1"
Movement_2_2 = RDK.Item("movement_2_2") ### MODIFIQUEM "Give5" PER "movement_2_2"

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
    print("Cane delivering")
    robot.MoveL(Movement_1_0, True)
    robot.MoveL(Movement_1_1, True)
    robot.MoveL(Movement_1_2, True)
    robot.MoveL(Movement_1_3, True)
    robot.MoveL(Movement_1_4, True)
    robot.MoveL(Movement_1_3, True)
    print("Cane delivering FINISHED")

# Perform "Give me 5" sequence
### CANVIEM "Give me 5" PER "Helping to get up"
def movement_2():
    print("Helping to get up")
    robot.MoveL(Movement_2_1, True)
    robot.MoveL(Movement_2_2, True)
    robot.MoveL(Movement_2_1, True)
    print("Helping to get up FINISHED")

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
