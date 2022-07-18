import tkinter as tk
from tkinter import ttk


class Status(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.progress_val = tk.StringVar()
        self.status = tk.StringVar()
        self.err_status = tk.StringVar()
        self.total_files = tk.StringVar()
        style = ttk.Style(self)
        style.configure('Green.TLabel', foreground='green')
        style.configure('Red.TLabel', foreground='red')
        status_frame = ttk.Frame(self)
        status_frame.grid(row=0, column=2, pady=20)
        self.status_label = ttk.Label(status_frame, text='', textvariable=self.status, style='Green.TLabel')
        self.status_label.grid(row=0, column=0)
        self.current_progress_label = ttk.Label(status_frame, text='', textvariable=self.progress_val,
                                                style='Green.TLabel')
        self.current_progress_label.grid(row=0, column=1)
        self.total_files_label = ttk.Label(status_frame, text='', textvariable=self.total_files, style='Green.TLabel')
        self.total_files_label.grid(row=0, column=2)
        self.status_label = ttk.Label(status_frame, text='', textvariable=self.err_status, style='Red.TLabel')
        self.status_label.grid(row=1, column=0)
        self.current = 0
        self.total = 0

    def set_error_status(self, e):
        self.err_status.set(e)

    def set_status_label(self, nof):
        """

        :rtype: object
        """
        self.status.set("Files Processed: ")
        self.total_files.set('/'+str(nof))
        self.total = nof
        self.current = 0
        # self.master.update_idletasks()

    def update_status(self):
        if self.current < self.total:
            self.current += 1
            self.progress_val.set(str(self.current))
            self.master.update_idletasks()
        else:
            self.progress_val.set(str(self.current))
            self.master.update_idletasks()
            self.current = 0
            self.total = 0
