import tkinter as tk
import serial
import threading
import time
import queue

class RobotHeadControlGUI:
    def __init__(self, root, command_queue):
        self.root = root
        self.command_queue = command_queue

        self.root.title("Robot Head Control")
        self.root.geometry("400x400")
        self.root.configure(bg="#800000")

        self.connection_status = tk.Label(self.root, text="Arduino Not Connected", fg="red")
        self.connection_status.pack()

        self.create_buttons()

    def create_buttons(self):
        reset_button = tk.Button(self.root, text="RESET", command=self.send_reset_command)
        reset_button.pack()

        cw_button = tk.Button(self.root, text="CW", command=self.send_cw_command)
        cw_button.pack()

        ccw_button = tk.Button(self.root, text="CCW", command=self.send_ccw_command)
        ccw_button.pack()

        angle_button = tk.Button(self.root, text="Get Angle", command=self.send_get_angle_command)
        angle_button.pack()

        direction_button = tk.Button(self.root, text="Get Direction", command=self.send_get_direction_command)
        direction_button.pack()

    def send_reset_command(self):
        self.command_queue.put("RESET")

    def send_cw_command(self):
        self.command_queue.put("CW")

    def send_ccw_command(self):
        self.command_queue.put("CCW")

    def send_get_angle_command(self):
        self.command_queue.put("GET_ANGLE")

    def send_get_direction_command(self):
        self.command_queue.put("GET_DIRECTION")

def control_motor(command_queue):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        gui.connection_status.pack_forget()  
    except serial.SerialException:
        ser = None  

    while True:
        if ser:
            try:
                command = command_queue.get(timeout=0.1)  
                ser.write(command.encode())
                print(f"Sent command: {command}")
                time.sleep(0.1)  
            except queue.Empty:
                pass  
        else:
            print("Arduino not connected")

if __name__ == "__main__":
    command_queue = queue.Queue()

    root = tk.Tk()
    gui = RobotHeadControlGUI(root, command_queue)

    motor_thread = threading.Thread(target=control_motor, args=(command_queue,))
    motor_thread.start()

    root.mainloop()
