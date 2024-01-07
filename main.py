import tkinter as tk
from tkinter import ttk, filedialog
import mido
from mido import MidiFile, MidiTrack, Message
import threading
import random
import time
import pygame
directions = ['↑', '↓', '←', '→']


class MyMidiApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Disorientation 迷失方向")

        self.flag = 0
        self.create_toolbar()
        self.create_widgets()
        self.setup_keyboard_bindings()
    
    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
    
        # MIDI Output Port
        self.output_label = ttk.Label(self.toolbar, text="Output Port:")
        self.output_label.pack(side=tk.LEFT, padx=5)
        self.output_var = tk.StringVar(self.master)
        self.output_ports = mido.get_output_names()
        self.output_dropdown = ttk.Combobox(self.toolbar, textvariable=self.output_var, values=self.output_ports)
        self.output_dropdown.pack(side=tk.LEFT)
        self.output_dropdown.set("Select Output Port")

        # MIDI File Selection
        self.file_btn = ttk.Button(self.toolbar, text="Select MIDI File", command=self.select_midi_file)
        self.file_btn.pack(side=tk.LEFT, padx=10)

        # finish Button
        self.finish_button = ttk.Button(self.toolbar, text="Finish Game Play", command=self.destroy)
        self.finish_button.pack(side=tk.RIGHT,pady=10)

    def create_widgets(self):
        # main appearence
        self.direction_frame = ttk.Frame(self.master)
        self.direction_frame.pack(pady=10)

        # 上
        self.up_button = ttk.Button(self.direction_frame, text = "↑", command=lambda:self.next_second("↑"))
        self.up_button.grid(row=0, column=1)

        # 下
        self.down_button = ttk.Button(self.direction_frame, text = "↓", command=lambda:self.next_second("↓"))
        self.down_button.grid(row=2, column=1)
        
        # 左
        self.left_button = ttk.Button(self.direction_frame, text = "←", command=lambda:self.next_second("←"))
        self.left_button.grid(row=1, column=0)
        
        # 右
        self.right_button = ttk.Button(self.direction_frame, text = "→", command=lambda:self.next_second("→"))
        self.right_button.grid(row=1, column=2)

        # 首先顯示第一個隨機方向
        self.random_choice = random.choice(directions)
        self.question = ttk.Label(self.direction_frame, text = self.random_choice)
        self.question.grid(row=1, column=1)
        
    def next_second(self,button_id):
        # 若答對可以前進5秒，答錯則是不動
        if(button_id == self.random_choice):
            self.random_choice = random.choice(directions)
            self.question.config(text=self.random_choice)
            self.flag = 1
            pygame.mixer.music.unpause()
            time.sleep(3)
            pygame.mixer.music.pause()
            
        
    def setup_keyboard_bindings(self):
        # 搭配鍵盤功能
        self.master.bind("<Up>", lambda event: self.next_second("↑"))
        self.master.bind("<Down>", lambda event: self.next_second("↓"))
        self.master.bind("<Left>", lambda event: self.next_second("←"))
        self.master.bind("<Right>", lambda event: self.next_second("→"))
    
    def select_midi_file(self):
        # 選擇要撥放的midi檔
        file_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.midi;*.mid")])
        if file_path:
            print(f"Selected MIDI file: {file_path}")
            self.play_midi_file(file_path)

    def play_midi_file(self, file_path):
        
        # mid = MidiFile(file_path)

        # def play_thread():
        #     for msg in mid.play():
        #         # if self.flag:
        #             # print("答對")
        #             if msg.type == 'note_on' or msg.type == 'note_off':
        #                 midi_out.send(msg)
        #             # time.sleep(1)
        #             self.flag = 0
                    
        # midi_out_port = self.output_var.get()
        # midi_out = mido.open_output(midi_out_port)

        # play_thread = threading.Thread(target=play_thread) 
        
        # print("ready?")
        # self.flag = 1
        # play_thread.start()
       
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        time.sleep(3)
        pygame.mixer.music.pause()
        # pygame.mixer.music.unpause()
        
    def destroy(self):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyMidiApp(root)
    root.mainloop()
