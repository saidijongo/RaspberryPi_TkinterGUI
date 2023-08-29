import serial
import tkinter as tk
from tkinter import ttk

class DaminRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Head Control")
        self.root.configure(bg="yellow")

        self.create_widgets()  # Call create_widgets first
        self.connect_to_arduino()  # Then connect_to_arduino

    def connect_to_arduino(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
            self.connection_status.config(text="Arduino Detected", fg="green")
        except serial.SerialException:
            self.connection_status.config(text="Arduino Not Connected", fg="red")

    def create_widgets(self):
        self.connection_status = tk.Label(self.root, text="Arduino Not Connected", fg="red", bg="yellow")
        self.connection_status.pack()

        self.reset_button = ttk.Button(self.root, text="RESET (R)", command=self.send_reset)
        self.reset_button.pack(padx=10, pady=10)

        self.cw_button = ttk.Button(self.root, text="CW 90° (C)", command=self.send_cw)
        self.cw_button.pack(padx=10, pady=10)

        self.ccw_button = ttk.Button(self.root, text="CCW 90° (D)", command=self.send_ccw)
        self.ccw_button.pack(padx=10, pady=10)

        self.info_button = ttk.Button(self.root, text="Info (I)", command=self.request_info)
        self.info_button.pack(padx=10, pady=10)

        self.angle_label = ttk.Label(self.root, text="Enter Angle:")
        self.angle_label.pack(padx=10, pady=10)

        self.angle_entry = ttk.Entry(self.root)
        self.angle_entry.pack(padx=10, pady=10)

        self.send_angle_button = ttk.Button(self.root, text="Send Angle", command=self.send_angle)
        self.send_angle_button.pack(padx=10, pady=10)

        self.status_label = ttk.Label(self.root, text="Status:")
        self.status_label.pack(padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for command...")
        self.status_display = ttk.Label(self.root, textvariable=self.status_var)
        self.status_display.pack(padx=10, pady=10)

    def send_command(self, command):
        if self.ser:
            self.ser.write(command.encode() + b'\n')
            self.status_var.set(f"Sent command: {command}")
        else:
            self.status_var.set("Arduino Not Connected")

    def send_reset(self):
        self.send_command("R")

    def send_cw(self):
        self.send_command("C")

    def send_ccw(self):
        self.send_command("D")

    def request_info(self):
        self.send_command("I")

    def send_angle(self):
        angle = self.angle_entry.get()
        if angle:
            self.send_command(angle)

    def close_serial(self):
        if self.ser:
            self.ser.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DaminRobot(root)
    root.protocol("WM_DELETE_WINDOW", app.close_serial)
    root.mainloop()
