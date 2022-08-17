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
        # opens second window with timer
        self.newWindow = tk.Toplevel(self.master)
        self.master.wm_state('iconic')
        self.app = Demo2(self.newWindow, float(self.entry_yellow.get()), float(self.entry_red.get()), 5)


class Demo2:
    def __init__(self, master, yellow_light, red_light, grey_light):
        self.master = master
        self.stop = 0
        self.master.overrideredirect(1)
        self.master.wm_geometry('125x75-50+25')
        # keep it on top of other windows always
        self.master.attributes('-topmost', 'True')
        # self.master.update()
        # self.master.attributes('-topmost', False)
        self.frame = tk.Frame(self.master)
        self.timer_frame = tk.Frame(self.master)

        # convert yellow light in minutes to seconds
        self.yellow_light_start = yellow_light*60
        self.red_light_start = red_light * 60
        self.grey_light_start = grey_light * 60

        print(self.yellow_light_start)
        self.red_light_start = red_light*60

        self.size = 100, 100
        self.logo_loc = Image.open("logo.png")
        self_logo_loc = self.logo_loc.thumbnail(self.size, Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo_loc)

        self.logo_label = tk.Label(self.frame, image=self.logo,)
        # self.master.bind("<KeyRelease-a>", self.key_press)
        self.logo_label.pack(side="top")

        #self.quitButton = tk.Button(self.frame, text='Quit', command = self.close_windows)
        #self.quitButton.pack(side="left")

        self.label_time = tk.StringVar()
        self.label_time.set("")
        self.labelDir_time = tk.Label(self.timer_frame, textvariable=self.label_time, bg='green', height=20, width=10)
        self.labelDir_time.pack(side="left")

        self.timer_text = tk.StringVar()
        self.timer = tk.Label(self.frame, textvariable=self.timer_text)
        self.timer.pack(side='bottom')


        self.frame.pack(side='left')
        self.timer_frame.pack(side='left')
        self.timer_text.set('0:00')




        # shift q can quit
        keyboard.add_hotkey('shift+q', lambda: self.master.overrideredirect(0))
        # shift w hide top bar
        keyboard.add_hotkey('shift+w', lambda: self.master.overrideredirect(1))
        # shift s start
        keyboard.add_hotkey('shift+s', self.start_timer)


    def change_color(self, bg):
        # change color is more like flash
        self.current_color = self.labelDir_time.cget("background")
        self.next_color = bg
        start = time.time()
        while start + 1 > time.time():
            # self.time_elapsed = round(time.time()-self.start_time)
            # minutes, seconds = divmod(self.time_elapsed, 60)
            # self.timer_text.set("{:0>1}:{:02.0f}".format(int(minutes), seconds))
            if keyboard.is_pressed('shift+d'):
                time.sleep(0.2)
                self.stop = 1
                break
        self.labelDir_time.config(background=self.next_color)
        while start + 2 > time.time():
            # self.time_elapsed = round(time.time()-self.start_time)
            # minutes, seconds = divmod(self.time_elapsed, 60)
            # self.timer_text.set("{:0>1}:{:02.0f}".format(int(minutes), seconds))
            if keyboard.is_pressed('shift+d'):
                time.sleep(0.2)
                self.stop = 1
                break
        self.labelDir_time.config(background=self.current_color)
        # self.master.after(1000, lambda: self.labelDir_time.config(background=self.current_color))

    def start_timer(self):
        self.timer_text.set('0:00')

        self.stop = 0
        # self.labelDir_time.config(background='green')
        # self.change_color()
        # time.sleep(self.yellow_light_start)
        # self.labelDir_time.config(background='yellow')S
        # time.sleep(self.red_light_start - self.yellow_light_start - 30)
        # self.change_color()
        # time.sleep(30)
        # self.labelDir_time.config(background='red')
        self.labelDir_time.config(background='green')
        self.change_color('grey')
        self.start_time = time.time()

        # turn light yellow

        while True:
            time.sleep(0.2)
            self.time_elapsed = round(time.time()-self.start_time)
            minutes, seconds = divmod(self.time_elapsed, 60)
            self.timer_text.set("{:0>1}:{:02.0f}".format(int(minutes), seconds))
            # print("{:0>1}:{:05.2f}".format(int(minutes), seconds))
            # print(start_time + self.yellow_light_start < time.time())
            if self.stop == 1:
                self.change_color('blue')
                break
            if self.start_time + self.yellow_light_start < time.time() <= self.start_time + self.red_light_start:
                self.labelDir_time.config(background='yellow')
            elif self.start_time + self.red_light_start < time.time() <= self.start_time + self.grey_light_start:
                self.labelDir_time.config(background='red')

            elif self.start_time + self.grey_light_start <= time.time():
                self.labelDir_time.config(background='grey')
                # self.labelDir_time.config(background='red')
                break
            if keyboard.is_pressed('shift+d'):
                self.change_color('blue')
                break

        # # wait to flash yellow
        # timeout = time.time()+self.flash_yellow_light - self.yellow_light_start
        # while True:
        #     time.sleep(0.1)
        #     # self.change_color('grey')
        #     if stop == 1:
        #         break
        #     if time.time() > timeout:
        #         break
        #     if keyboard.is_pressed('shift+d'):
        #         stop = 1
        #         break
        #
        # # flash yellow gray
        # timeout = time.time() + self.flash_yellow_red - self.flash_yellow_light
        # while True:
        #     time.sleep(0.1)
        #     self.change_color('grey')
        #     if stop == 1:
        #         break
        #     if time.time() > timeout:
        #         break
        #     if keyboard.is_pressed('shift+d'):
        #         stop = 1
        #         break
        #
        # # flash yellow red
        # timeout = time.time() + self.flash_red_light - self.flash_yellow_red
        # while True:
        #     time.sleep(0.1)
        #     self.change_color('red')
        #     if stop == 1:
        #         break
        #     if time.time() > timeout:
        #         self.labelDir_time.config(background='red')
        #         break
        #     if keyboard.is_pressed('shift+d'):
        #         stop = 1
        #         break
        #
        # # flash red gray
        # timeout = time.time() + self.red_light_start- self.flash_red_light
        # while True:
        #     time.sleep(0.1)
        #     self.change_color('grey')
        #     if stop == 1:
        #         break
        #     if time.time() > timeout:
        #         self.labelDir_time.config(background='red')
        #         break
        #     if keyboard.is_pressed('shift+d'):
        #         stop = 1
        #         break




        # self.master.after(int(self.yellow_light_start), lambda: self.labelDir_time.config(background='yellow'))
        # self.master.after(int(5*1000), self.change_color)
        # self.master.after(int(self.red_light_start-self.yellow_light_start-30*1000),
        #                  lambda: self.labelDir_time.config(background='red'))





    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Demo2(root, 0.5, 1, 1.5)
    root.mainloop()

if __name__ == '__main__':
    main()