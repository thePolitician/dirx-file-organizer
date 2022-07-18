import threading
import tkinter as tk
from tkinter import ttk
import subprocess
import shutil
import os
from pathlib import Path


class ClearTemp(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.dir_size = tk.StringVar()
        self.free_size = tk.StringVar()
        self.columnconfigure(0, weight=1)
        self.path = (os.path.expanduser('~'))+'\\AppData\\Local\\Temp'
        self.temp_path = tk.StringVar(value=self.path)
        main = ttk.Frame(self, padding=(30, 15))
        main.grid(row=0, column=0, sticky='NSEW')
        self.path_label = ttk.Label(main, text="Temp Directory:")
        self.path_label.grid(row=0, column=0, padx=10, pady=20, sticky="W")
        self.path_entry = ttk.Entry(main, width=40, textvariable=self.temp_path, state='disabled')
        self.path_entry.grid(row=0, column=1, padx=5, pady=20, sticky="WE")
        self.open_button = ttk.Button(main, text="Open Folder", command=self.open_temp)
        self.open_button.grid(row=0, column=2, padx=5, sticky="W")
        self.clear_button = ttk.Button(main, text="Clear Temp", command=self.start_clear_temp)
        self.clear_button.grid(row=1, column=1, padx=20)
        size_frame = ttk.Frame(main)
        size_frame.grid(row=2, column=1, pady=20)
        self.size_label = ttk.Label(size_frame, text='Size: ', style='Green.TLabel')
        self.size_label.grid(row=0, column=0, pady=10, sticky='e')
        self.size_mb = ttk.Label(size_frame, text='', textvariable=self.dir_size, style='Green.TLabel')
        self.size_mb.grid(row=0, column=1, pady=10, sticky='w')
        self.dir_size.set(f"{self.get_size(self.path):.2f} MB")
        self.free_size_label = ttk.Label(size_frame, text='Space Freed: ', style='Green.TLabel')
        self.free_size_label.grid(row=1, column=0, pady=5)
        self.free_size_mb = ttk.Label(size_frame, text='', textvariable=self.free_size, style='Green.TLabel')
        self.free_size_mb.grid(row=1, column=1, pady=5)

    def start_clear_temp(self):
        new_thread = threading.Thread(target=self.clear_temp)
        new_thread.start()

    def clear_temp(self):
        self.clear_button["state"] = "disabled"
        total_size = self.get_size(self.path)
        if os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)
            try:
                os.mkdir(self.path)
            except FileExistsError:
                pass
        else:
            pass
        self.clear_button["state"] = "enabled"
        size = self.get_size(self.path)
        self.dir_size.set(f"{size:.2f} MB")
        self.free_size.set(f"{total_size-size:.2f} MB")

    def open_temp(self):
        if os.path.exists(self.path):
            subprocess.Popen(f'explorer {self.path}')
        else:
            pass

    def get_size(self, directory):
        root_directory = Path(directory)
        total = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
        total_mb = total/1048576
        return total_mb

