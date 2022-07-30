import tkinter as tk
from PIL import ImageTk, Image
import keyboard
import time

class Demo1:
    # class is used for input window
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        # yellow light
        self.yellow_frame = tk.Frame(self.frame)
        self.label_yellow = tk.StringVar()
        self.label_yellow.set("Yellow warning")
        self.labelDir_yellow = tk.Label(self.yellow_frame, textvariable=self.label_yellow)
        self.labelDir_yellow.pack(side="left")

        self.time_yellow = tk.StringVar(None)
        self.entry_yellow = tk.Entry(self.yellow_frame, textvariable=self.time_yellow, width=20)
        self.entry_yellow.pack(side="left")

        # red light
        self.red_frame = tk.Frame(self.frame)
        self.label_red = tk.StringVar()
        self.label_red.set("red warning")
        self.labelDir_red = tk.Label(self.red_frame, textvariable=self.label_red)
        self.labelDir_red.pack(side="left")

        self.time_red = tk.StringVar(None)
        self.entry_red = tk.Entry(self.red_frame, textvariable=self.time_red, width=20)
        self.entry_red.pack(side="left")

        # button, will create new window on completion
        self.button1 = tk.Button(self.frame, text='RUN', width = 25, command=self.new_window)

        # organize (can switch to grid view to align things/make less janky)
        self.yellow_frame.pack()
        self.red_frame.pack()
        self.frame.pack()
        self.button1.pack()

    def new_window(self):
        # opens second window
        self.newWindow = tk.Toplevel(self.master)
        self.master.wm_state('iconic')
        self.app = Demo2(self.newWindow, float(self.entry_yellow.get()), float(self.entry_red.get()))


class Demo2:
    def __init__(self, master, yellow_light, red_light):
        self.master = master
        self.master.overrideredirect(1)
        self.master.wm_geometry('200x100-60-50')
        # keep it on top of other windows always
        self.master.attributes('-topmost', 'True')
        # self.master.update()
        # self.master.attributes('-topmost', False)
        self.frame = tk.Frame(self.master)
        self.yellow_light_start = yellow_light*60
        print(self.yellow_light_start)
        self.red_light_start = red_light*60
        self.size = 150, 150
        self.logo_loc = Image.open("logo.png")
        self_logo_loc = self.logo_loc.thumbnail(self.size, Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo_loc)

        self.logo_label = tk.Label(self.frame, image=self.logo,)
        # self.master.bind("<KeyRelease-a>", self.key_press)
        self.logo_label.pack(side="left")

        #self.quitButton = tk.Button(self.frame, text='Quit', command = self.close_windows)
        #self.quitButton.pack(side="left")

        self.time_frame = tk.Frame(self.frame)
        self.label_time = tk.StringVar()
        self.label_time.set("")
        self.labelDir_time = tk.Label(self.frame, textvariable=self.label_time, bg='green', height=200, width=50)
        self.labelDir_time.pack(side="left")
        self.frame.pack()

        keyboard.add_hotkey('shift+q', lambda: self.master.overrideredirect(0))
        keyboard.add_hotkey('shift+w', lambda: self.master.overrideredirect(1))
        keyboard.add_hotkey('shift+s', self.start_timer)

    def change_color(self):
        self.current_color = self.labelDir_time.cget("background")
        self.next_color = "grey"
        self.labelDir_time.config(background=self.next_color)
        self.master.after(1000, lambda: self.labelDir_time.config(background=self.current_color))

    def start_timer(self):
        self.labelDir_time.config(background='green')
        self.change_color()
        time.sleep(self.yellow_light_start)
        self.labelDir_time.config(background='yellow')
        time.sleep(30)
        self.change_color()
        time.sleep(self.red_light_start- self.yellow_light_start - 30)
        self.labelDir_time.config(background='red')

        # self.master.after(int(self.yellow_light_start), lambda: self.labelDir_time.config(background='yellow'))
        # self.master.after(int(5*1000), self.change_color)
        # self.master.after(int(self.red_light_start-self.yellow_light_start-30*1000),
        #                  lambda: self.labelDir_time.config(background='red'))








    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()