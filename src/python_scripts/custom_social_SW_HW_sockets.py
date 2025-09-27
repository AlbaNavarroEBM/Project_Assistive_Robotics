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

# URScript commands
# canviar joint positions
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
movej_init = f"movej([-1.009423, -1.141297, -1.870417, 3.011723, -1.009423, 0.000000],1.20000,0.75000,{timel},0.0000)"
movel_give_paw_app = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel},0.000)"
movel_give_paw = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel/2},0.000)"
movel_good_boy_app = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel},0.000)"
movel_good_boy_1 = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel/2},0.000)"
movel_good_boy_2 = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel/2},0.000)"
movel_good_boy_3 = f"movel([TODO_JOINT_POSITIONS],{accel_mss},{speed_ms},{timel/2},0.000)"

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
        receive_response(timej)
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
        receive_response(timel)
        send_ur_script(movel_give_paw)
        receive_response(timel)
        send_ur_script(movel_give_paw_app)
        receive_response(timel)

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
        receive_response(timel)
        send_ur_script(movel_good_boy_1)
        receive_response(timel)
        send_ur_script(movel_good_boy_2)
        receive_response(timel)
        send_ur_script(movel_good_boy_1)
        receive_response(timel)
        send_ur_script(movel_good_boy_3)
        receive_response(timel)
        send_ur_script(movel_good_boy_1)
        receive_response(timel)
        send_ur_script(movel_good_boy_app)
        receive_response(timel)

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
    move_to_init()
    if robot_is_connected:
        robot_socket.close()

# Run and close
if __name__ == "__main__":
    main()
    confirm_close()
