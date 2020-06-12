import threading
import time
import datetime
import sqlite3
import os
import tkinter as tk
from tkinter import messagebox as msg

class CountingThread(threading.Thread):
    def __init__(self, master, start_time , end_time):
        super().__init__()
        self.master = master 
        self.start_time = start_time
        self.end_time = end_time

        self.end_now = False
        self.paused = False
        self.force_quit = False
    def run(self):
        while True:
            if not self.paused and not self.end_now and not self.force_quit:
                self.main_loop()
                if datetime.datetime.now()>=self.end_time:
                    if not self.force_quit:
                        self.master.finish()
                        break
            elif self.end_now:
                self.master.finish()
                break
            elif self.force_quit:
                del self.master.counterTime
                return
            else:
                continue
        return
    def main_loop(self) :
        now = datetime.datetime.now()
        if now < self.end_time:
            time_difference = self.end_time - now 
            hours , remainder = divmod(time_difference.seconds, 3600)
            mins , secs  = divmod(remainder,60)
            time_string = "{:02d}:{:02d}".format(mins,secs)
            if not self.force_quit:
                self.master.update_time_remaining(time_string)




class Timer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")
        self.geometry("500x300")
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=500, height=300, bg="lightgrey")

        self.task_name_label = tk.Label(self.main_frame, text="Task Name:", bg="lightgrey", fg="black", font=self.standard_font)
        self.task_name_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)
        self.start_button = tk.Button(self.main_frame, text="Start", bg="lightgrey", fg="black", command=self.start, font=self.standard_font)
        self.time_remaining_var = tk.StringVar(self.main_frame)
        self.time_remaining_var.set("25:00")
        self.time_remaining_label = tk.Label(self.main_frame, textvar=self.time_remaining_var, bg="lightgrey", fg="black", font=(None, 40,"bold"))
        self.pause_button = tk.Button(self.main_frame, text="Pause", bg="lightgrey", fg="black", command=self.pause, font=self.standard_font, state="disabled")

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.task_name_label.pack(fill=tk.X, pady=15)
        self.task_name_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.start_button.pack(fill=tk.X, padx=50)
        self.time_remaining_label.pack(fill=tk.X ,pady=15)
        self.pause_button.pack(fill=tk.X, padx=50)

        self.bind("<Control-l>", self.show_log_window)
    def setup_counter_time(self):
        now = datetime.datetime.now()
        En25mins = now + datetime.timedelta(minutes=25)
        counterTime = CountingThread(self,now,En25mins)
        self.counterTime = counterTime
        self.start_time = now

    def start(self):
        if not hasattr(self, "counterTime"):
            self.setup_counter_time()
        if self.start_button.cget("text")=="Finish":
            self.start_button.configure(text="Restart")
            self.counterTime.end_now = True
        elif self.start_button.cget("text")=="Restart":
            self.setup_counter_time()
            self.restart()
        else:
            self.start_button.cget("text") == "Start"
            self.task_name_entry.configure(state = "disable")
            self.start_button.configure(text="Finish")
            self.time_remaining_var.set("25:00")
            self.pause_button.configure(state = "normal")
            self.add_task_to_db()
            self.counterTime.start()

             
        

    def pause(self):
        
        self.counterTime.paused = not self.counterTime.paused
        if self.counterTime.paused:
            self.pause_button.configure(text="Resume")
            self.counterTime.start_time = datetime.datetime.now()
        else:
            self.pause_button.configure(text="Pause")
            end_deltaTime = datetime.datetime.now() - self.counterTime.start_time
            self.counterTime.end_time = self.counterTime.end_time + datetime.timedelta(seconds=end_deltaTime.seconds)
    
    def show_log_window(self):
        pass
    def add_task_to_db(self):
        pass
    def mark_task_as_completed(self):
        pass
    def update_time_remaining(self,timeString):
        self.time_remaining_var.set(timeString)
    def restart(self):
        self.task_name_entry.configure(state = "disabled")
        self.start_button.configure(text="Finish")
        self.time_remaining_var.set("25:00")
        self.add_task_to_db()
        self.counterTime.start()

    def finish(self):
        self.mark_task_as_completed()
        self.task_name_entry.configure(text="normal")
        self.time_remaining_var.set("25:00")
        self.pause_button.configure(state="disabled")
        msg.showinfo("Tarea Terminada", " Take a break")

        

if __name__ == "__main__":
    timer = Timer()
    timer.mainloop()