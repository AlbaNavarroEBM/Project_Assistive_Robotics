import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

# Load RoboDK project from relative path
relative_path = "src/roboDK/GoodBoy.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()

# Robot setup
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
Give_paw_app = RDK.Item('Give_paw_approach')
Give_paw = RDK.Item('Give_paw')
Good_boy_app = RDK.Item('Good_boy_approach')
Good_boy_1 = RDK.Item('Good_boy_1')
Good_boy_2 = RDK.Item('Good_boy_2')
Good_boy_3 = RDK.Item('Good_boy_3')
Sit_1= RDK.Item("Give_paw_approach") 
Sit_2= RDK.Item("Sit_2")

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 4

def movej_from_target(target, accel=accel_mss, speed=speed_ms, tim=timej, blend=blend_r):
    """Return a URScript movej command string for the given RoboDK target (in joint space)."""
    if not target.Valid():
        raise ValueError(f"Target {target.Name()} is not valid")
    
    # Get the joints of the target in radians
    j1, j2, j3, j4, j5, j6 = np.radians(target.Joints()).tolist()[0]

    return (
        f"movej([{j1:.6f}, {j2:.6f}, {j3:.6f}, {j4:.6f}, {j5:.6f}, {j6:.6f}], "
        f"a={accel}, v={speed}, t={tim}, r={blend})"
    )

# URScript commands
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
movej_init = f"movej([-1.009423, -1.141297, -1.870417, 3.011723, -1.009423, 0.000000],1.20000,0.75000,{timel},0.0000)"
movel_give_paw_app = movej_from_target(Give_paw_app, tim=timel)
movel_give_paw     = movej_from_target(Give_paw, tim=timel/2)

movel_good_boy_app = movej_from_target(Good_boy_app, tim=timel)
movel_good_boy_1   = movej_from_target(Good_boy_1, tim=timel/2)
movel_good_boy_2   = movej_from_target(Good_boy_2, tim=timel/2)
movel_good_boy_3   = movej_from_target(Good_boy_3, tim=timel/2)
movel_sit_1= movej_from_target(Sit_1, tim=timel/2)
movel_sit_2=movej_from_target(Sit_2, tim=timel/2)

# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

# Wait for robot response
def receive_response(t):
    try:
        print("Waiting time:", t)
        time.sleep(t)
    except socket.error as e:
        print(f"Error receiving data: {e}")
        exit(1)

# Movements
def move_to_init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    if robot_is_connected:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init)
        receive_response(1) ## modificat: timel-->1
    else:
        print("UR5e not connected. Simulation only.")

def movement_1():
    print("Give me paw")
    robot.setSpeed(20)
    robot.MoveL(Give_paw_app, True)
    robot.setSpeed(100)
    robot.MoveL(Give_paw, True)
    robot.MoveL(Give_paw_app, True)
    print("Give me paw FINISHED")
    if robot_is_connected:
        print("Give_paw REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_give_paw_app)
        receive_response(1) ## modificat: timel-->1
        send_ur_script(movel_give_paw)
        receive_response(timel)
        send_ur_script(movel_give_paw_app)
        receive_response(2) ## modificat: timel-->2

def movement_2():
    print("Who is a good boy?!")
    robot.setSpeed(20)
    robot.MoveL(Good_boy_app, True)
    robot.setSpeed(100)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_2, True)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_3, True)
    robot.MoveL(Good_boy_1, True)
    robot.MoveL(Good_boy_app, True)
    print("Good boy FINISHED")
    if robot_is_connected:
        print("Good_boy REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_good_boy_app)
        receive_response(1) ## modificat: timel-->1
        send_ur_script(movel_good_boy_1)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_good_boy_2)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_good_boy_1)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_good_boy_3)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_good_boy_1)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_good_boy_app)
        receive_response(2) ## modificat: timel-->2

def movement_3():
    print("Sit!")
    robot.setSpeed(20)
    robot.MoveL(Good_boy_app, True) 
    robot.setSpeed(100)
    robot.MoveL(Sit_1, True)
    robot.MoveL(Sit_2, True)
    robot.MoveL(Good_boy_app, True)
    print("Sit FINISHED")
    if robot_is_connected:
        print("Sit REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        #send_ur_script(movel_good_boy_app)###crec que no cal
        #receive_response(1)
        send_ur_script(movel_sit_1)
        receive_response(0.5) ## modificat: timel-->0.5
        send_ur_script(movel_sit_2)
        receive_response(2) ## modificat: timel-->2
        #send_ur_script(movel_good_boy_app)###crec que no cal
        #receive_response(1)

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
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    move_to_init()
    movement_1()
    movement_2()
    movement_3()
    movement_2()
    move_to_init()
    if robot_is_connected:
        robot_socket.close()

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()
