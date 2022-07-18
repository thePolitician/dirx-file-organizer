import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import shutil


def disable(frame):
    for child in frame.winfo_children():
        child.configure(state='disabled')


def enable(frame):
    for child in frame.winfo_children():
        child.configure(state='enabled')


class DirUnpack(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.success_status = tk.StringVar()
        self.fail_status = tk.StringVar()
        self.del_folders = tk.BooleanVar(value=False)
        self.home_dir = (os.path.expanduser('~')) + '\\Desktop'
        os.chdir(self.home_dir)
        self.path = tk.StringVar(value=self.home_dir)
        # style = ttk.Style(self)
        # style.configure('My.TFrame', background='white')
        self.main = ttk.Frame(self, padding=(30, 15))
        self.main.grid(row=0, column=0, sticky='NSEW')
        style = ttk.Style(self)
        style.configure('Green.TLabel', foreground='green')
        style.configure('Red.TLabel', foreground='red')
        self.columnconfigure(0, weight=1)
        self.path_label = ttk.Label(self.main, text="Parent Directory:")
        self.path_label.grid(row=0, column=0, padx=10, pady=20, sticky="W")
        self.path_entry = ttk.Entry(self.main, width=40, textvariable=self.path)
        self.path_entry.grid(row=0, column=1, padx=5, pady=20, sticky="WE")
        self.select_button = ttk.Button(self.main, text="Select Folder", command=self.open_dialog)
        self.select_button.grid(row=0, column=2, padx=5, sticky="W")
        self.unpack_button = ttk.Button(self.main, text="Unpack", command=self.start_unpack)
        self.unpack_button.grid(row=1, column=1, padx=20)
        self.del_check = ttk.Checkbutton(self.main, text="Delete emptied folders",
                                         variable=self.del_folders, onvalue=True, offvalue=False)
        self.del_check.grid(row=2, column=1, pady=5)
        success_label = ttk.Label(self.main, textvariable=self.success_status, style='Green.TLabel')
        success_label.grid(row=3, column=1, pady=5)
        fail_label = ttk.Label(self.main, textvariable=self.fail_status, style='Red.TLabel')
        fail_label.grid(row=4, column=1, pady=5)

    def start_unpack(self):
        new_thread = threading.Thread(target=self.unpack_files)
        new_thread.start()

    def unpack_files(self):
        disable(self.main)
        path = self.path.get()

        if os.path.exists(path):
            count = 0
            total = 0
            self.success_status.set('Unpacking...')
            self.update_idletasks()
            self.select_button["state"] = "disabled"
            self.unpack_button["state"] = "disabled"
            self.del_check["state"] = "disabled"
            list_ = [dir_ for dir_ in os.listdir(path) if os.path.isdir(dir_)]
            for dir_ in list_:
                file_list = os.listdir(path+'/'+dir_)
                for afile in file_list:
                    total += 1
                    try:
                        shutil.move(path + '/' + dir_ + '/' + afile, path)
                        count += 1
                    except: pass
                if self.del_folders.get():
                    try:
                        os.rmdir(path + '/' + dir_)
                    except: pass
            self.success_status.set(f"Files Unpacked: {count}/{total}")
        else:
            self.fail_status.set("Path not found!")
        enable(self.main)


    def open_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            os.chdir(folder_path)
            self.path.set(folder_path)
        elif not self.path.get():
            self.path.set(self.home_dir)
            