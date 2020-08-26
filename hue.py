from phue import Bridge
import tkinter as tk
from tkinter import *

class HueApp:

    def __init__(self, parent):
        self.bridge = Bridge('192.168.0.4')

        self.lights = self.bridge.get_light_objects('name')

        self.root = parent

        self.labels = {}
        self.vars = {}
        self.scaleValues = {}
        self.names = []
        self.mousePressed = 0

        self.top = tk.Frame(parent)

        self.root.title("Light Control")
        self.top.bind("<Button-1>", self.left_click)
        self.top.bind("<ButtonRelease-1>", self.left_release)
        self.create_controls()
        self.check_light()

        self.top.pack()

    def check_light(self):
        if not self.mousePressed:
            value = 0
            for name, label in self.labels.items():
                if self.lights[name].on:
                    self.vars[name].set("On")
                    label.configure(bg='green')
                else:
                    self.vars[name].set("Off")
                    label.configure(bg='red')
            self.top.after(500, self.check_light)

    def dim(self, percent, name):
        if self.lights[name].on:
            self.bridge.set_light(name, 'on', True)
            value = 254/100 * int(percent)
            self.lights[name].brightness = int(value)

    def light_on(self, name):
        self.lights[name].on = True

    def light_off(self, name):
        self.lights[name].on = False

    def left_click(self, event):
        self.mousePressed = 1

    def left_release(self, event):
        self.mousePressed = 0
        self.check_light()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def create_controls(self):
        buttons = []
        scales = []
        padx = 5
        pady = 5
        ipadx = 5
        ipady = 5

        for light in self.bridge.lights:
            light_name = light.name
            self.vars[light_name] = StringVar()
            self.scaleValues[light_name] = IntVar()
            label = Label(self.top, text=light_name, height=2)
            buttons.append(Button(self.top, text="On", command=lambda arg=light_name: self.light_on(arg)))
            buttons.append(Button(self.top, text="Off", command=lambda arg=light_name: self.light_off(arg)))
            self.labels[light_name] = (Label(self.top, textvariable=self.vars[light_name]))
            scales.append(Scale(self.top, orient=HORIZONTAL, length=200, repeatdelay=300, command=lambda arg=0, arg2=light_name: self.dim(arg, arg2)))
            self.names.append(light_name)

            label.grid(row=light.light_id, column=1, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
            buttons[-2].grid(row=light.light_id, column=2, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
            buttons[-1].grid(row=light.light_id, column=3, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
            self.labels[light_name].grid(row=light.light_id, column=4, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
            scales[-1].grid(row=light.light_id, column=5, padx=padx, pady=pady)

            # Set scale to correct value
            value = self.lights[light_name].brightness / 254 * 100
            scales[-1].set(value)


if __name__ == "__main__":
    root = tk.Tk()
    hue_app = HueApp(root)
    root.geometry('600x500+-1200+300')
    root.mainloop()
