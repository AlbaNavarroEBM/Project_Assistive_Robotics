import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/GoodBoy.rdk"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink(args=absolute_path)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
Give_paw_app = RDK.Item("Give_paw_approach")
Give_paw = RDK.Item("Give_paw") 
Good_boy_app = RDK.Item("Good_boy_approach") 
Good_boy_1 = RDK.Item("Good_boy_1")
Good_boy_2 = RDK.Item("Good_boy_2")
Good_boy_3 = RDK.Item("Good_boy_3") 
Sit_1= RDK.Item("Give_paw_approach")
Sit_2= RDK.Item("Sit_2")

# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)

# Connect to real robot or simulate
def robot_online(online):
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")

# Robot movements
def move_to_init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

def movement_1():
    print("Give me paw")
    robot.MoveL(Give_paw_app, True)
    robot.MoveL(Give_paw, True)
    robot.MoveL(Give_paw_app, True)
    print("Give me paw FINISHED")

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

def movement_3():
    print("Sit!")
    robot.MoveL(Good_boy_app, True)
    robot.MoveL(Sit_1, True)
    robot.MoveL(Sit_2, True)
    robot.MoveL(Good_boy_app, True)
    print("Sit FINISHED")

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

# Main function
def main():
    robot_online(False)  # True for real robot, False for simulation
    move_to_init()
    movement_1()
    movement_2()
    movement_3()
    movement_2()
    move_to_init()

# Run main and handle closing
if __name__ == "__main__":
    main()
    confirm_close()
