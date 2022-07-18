import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import datetime
from pathlib import Path
from Frames.status import Status


def disable(frame):
    for child in frame.winfo_children():
        child.configure(state='disabled')


def enable(frame, str):
    for child in frame.winfo_children():
        child.configure(state=str)


class BatchRename(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.home_dir = (os.path.expanduser('~')) + '\\Desktop'
        os.chdir(self.home_dir)
        self.add_prefix = tk.BooleanVar()
        self.change_fname = tk.BooleanVar()
        self.add_postfix = tk.BooleanVar()
        self.prefix_type = tk.StringVar()
        self.fname_type = tk.StringVar()
        self.postfix_type = tk.StringVar()
        self.custom_prefix_text = tk.StringVar()
        self.custom_fname_text = tk.StringVar()
        self.custom_postfix_text = tk.StringVar()
        self.path = tk.StringVar(value=self.home_dir)
        self.top_frame = ttk.Frame(self, padding=(10, 10))
        self.top_frame.grid(row=0, columnspan=2, sticky='NSEW')
        # self.main = ttk.Frame(self, padding=(10, 10))
        # self.main.grid(row=1, columnspan=2, sticky='NSEW')
        self.columnconfigure(0, weight=1)
        self.path_label = ttk.Label(self.top_frame, text="Parent Directory:")
        self.path_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.path_entry = ttk.Entry(self.top_frame, width=40, textvariable=self.path)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="WE")
        self.select_button = ttk.Button(self.top_frame, text="Select Folder", command=self.open_dialog)
        self.select_button.grid(row=0, column=2, padx=5, sticky="W")
        self.rename_button = ttk.Button(self.top_frame, text="Rename All", command=self.start_rename)
        self.rename_button.grid(row=1, column=1, padx=20, pady=10)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        #self.progress_bar.grid()

        self.check_frame = ttk.Frame(self)
        self.check_frame.grid(row=1, column=0, padx=5)
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.grid(row=1, column=1, padx=10)

        self.prefix_check_button = ttk.Checkbutton(self.check_frame, text='Add Prefix: ', variable=self.add_prefix,
                                                   onvalue=True, offvalue=False, command=self.set_prefix)
        self.prefix_check_button.grid(row=0, column=0, padx=10, pady=3, sticky='W')

        self.prefix_options = ttk.Combobox(self.check_frame, width=15, textvariable=self.prefix_type, state='disabled')
        self.prefix_options["values"] = ('Custom', 'Numeric', 'Date Created', 'Date Modified')
        self.prefix_options.current(0)
        self.prefix_options.grid(row=0, column=1, pady=3, sticky='W')
        self.prefix_options.bind("<<ComboboxSelected>>", self.OnSelectPrefix)

        self.custom_prefix_label = ttk.Label(self.entry_frame, text='Text: ')
        self.custom_prefix_label.grid(row=0, column=0, pady=3, sticky='W')
        self.custom_prefix_entry = ttk.Entry(self.entry_frame, width=25, textvariable=self.custom_prefix_text,
                                             state='disabled')
        self.custom_prefix_entry.grid(row=0, column=1, pady=3, sticky='W')

        self.change_fname_check_button = ttk.Checkbutton(self.check_frame, text='Change File Name: ',
                                                         variable=self.change_fname,
                                                         onvalue=True, offvalue=False, command=self.set_fname)
        self.change_fname_check_button.grid(row=1, column=0, padx=10, pady=3, sticky='W')

        self.fname_options = ttk.Combobox(self.check_frame, width=15, textvariable=self.fname_type, state='disabled')
        self.fname_options["values"] = ('Custom', 'Numeric', 'Date Created', 'Date Modified')
        self.fname_options.current(0)
        self.fname_options.grid(row=1, column=1, pady=3, sticky='W')
        self.fname_options.bind("<<ComboboxSelected>>", self.OnSelectName)

        self.custom_fname_label = ttk.Label(self.entry_frame, text='Text: ')
        self.custom_fname_label.grid(row=1, column=0, pady=3, sticky='W')

        self.custom_fname_entry = ttk.Entry(self.entry_frame, width=25, textvariable=self.custom_fname_text,
                                            state='disabled')
        self.custom_fname_entry.grid(row=1, column=1, pady=3, sticky='W')

        self.postfix_check_button = ttk.Checkbutton(self.check_frame, text='Add Postfix: ', variable=self.add_postfix,
                                                    onvalue=True, offvalue=False, command=self.set_postfix)
        self.postfix_check_button.grid(row=2, column=0, padx=10, pady=3, sticky='W')

        self.postfix_options = ttk.Combobox(self.check_frame, width=15, textvariable=self.postfix_type, state='disabled')
        self.postfix_options["values"] = ('Custom', 'Numeric', 'Date Created', 'Date Modified')
        self.postfix_options.current(0)
        self.postfix_options.grid(row=2, column=1, pady=3, sticky='W')
        self.postfix_options.bind("<<ComboboxSelected>>", self.OnSelectPostfix)

        self.custom_postfix_label = ttk.Label(self.entry_frame, text='Text: ')
        self.custom_postfix_label.grid(row=2, column=0, pady=3, sticky='W')
        self.custom_postfix_entry = ttk.Entry(self.entry_frame, width=25, textvariable=self.custom_postfix_text,
                                              state='disabled')
        self.custom_postfix_entry.grid(row=2, column=1, pady=3, sticky='W')
        self.status = Status(self)
        self.status.grid(row=2, columnspan=2)
        self.total_files = 0

    def start_rename(self):
        new_thread = threading.Thread(target=self.rename_all)
        #self.update_progress(new_thread, 0)
        new_thread.start()

    def update_progress(self, thread, step):
        while thread.isAlive() and step < self.total_files:
            self.progress_bar['value'] += step
            self.after(200, self.update_progress, step)

    def rename_all(self):
        self.disable_all()
        path = self.path.get()
        try:
            os.chdir(path)
        except FileNotFoundError:
            self.status.set_error_status("     Invalid Path!")
            self.enable_all()
            return
        list_ = [file_ for file_ in os.listdir(path) if os.path.isfile(file_)]
        prefix_index = -1
        fname_index = -1
        postfix_index = -1
        self.status.set_status_label(len(list_))

        for file_ in list_:
            prefix = ''
            fname, ext = os.path.splitext(file_)
            postfix = ''
            if self.add_prefix.get():
                prefix = f"{self.get_prefix(path, file_, prefix_index)} "
                prefix_index += 1
            if self.change_fname.get():
                fname = self.get_fname(path, file_, fname_index)
                fname_index += 1
            if self.add_postfix.get():
                postfix = f" {self.get_postfix(path, file_, postfix_index)}"
                postfix_index += 1

            dest = f"{prefix}{fname}{postfix}{ext}"
            src = file_
            try:
                os.rename(src, dest)
                self.status.update_status()
            except FileExistsError:
                i = 1
                while True:
                    try:
                        dest = f"{prefix}{fname}{postfix}({i}){ext}"
                        os.rename(src, dest)
                        break
                    except:
                        i += 1
                self.status.update_status()
        self.enable_all()

    def get_prefix(self, path, file_, i):
        if self.prefix_options.current() == 0:
            return self.custom_prefix_text.get()
        elif self.prefix_options.current() == 1:
            return i+1
        elif self.prefix_options.current() == 2:
            return self.get_doc(path, file_)
        elif self.prefix_options.current() == 3:
            return self.get_dom(path, file_)

    def get_fname(self, path, file_, i):
        if self.fname_options.current() == 0:
            return self.custom_fname_text.get()
        elif self.fname_options.current() == 1:
            return i+1
        elif self.fname_options.current() == 2:
            return self.get_doc(path, file_)
        elif self.fname_options.current() == 3:
            return self.get_dom(path, file_)

    def get_postfix(self, path, file_, i):
        if self.postfix_options.current() == 0:
            return self.custom_postfix_text.get()
        elif self.postfix_options.current() == 1:
            return i+1
        elif self.postfix_options.current() == 2:
            return self.get_doc(path, file_)
        elif self.postfix_options.current() == 3:
            return self.get_dom(path, file_)

    def set_prefix(self):
        if self.add_prefix.get():
            self.prefix_options["state"] = 'readonly'
            if self.prefix_options.current() == 0:
                self.custom_prefix_entry["state"] = 'enabled'
        else:
            self.prefix_options["state"] = 'disabled'
            self.custom_prefix_entry["state"] = 'disabled'

    def set_fname(self):
        if self.change_fname.get():
            self.fname_options["state"] = 'readonly'
            if self.fname_options.current() == 0:
                self.custom_fname_entry["state"] = 'enabled'
        else:
            self.fname_options["state"] = 'disabled'
            self.custom_fname_entry["state"] = 'disabled'

    def set_postfix(self):
        if self.add_postfix.get():
            self.postfix_options["state"] = 'readonly'
            if self.postfix_options.current() == 0:
                self.custom_postfix_entry["state"] = 'enabled'
        else:
            self.postfix_options["state"] = 'disabled'
            self.custom_postfix_entry["state"] = 'disabled'

    def open_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            os.chdir(folder_path)
            self.path.set(folder_path)
        elif not self.path.get():
            self.path.set(self.home_dir)

    def get_doc(self, path, file_):
        file = Path(os.path.join(path, file_))
        if os.path.exists(file):
            doc = datetime.datetime.fromtimestamp(file.stat().st_ctime)
            doc = doc.strftime('%d %b %Y')
            # doc = " ".join([str(doc.day), str(doc.month), str(doc.year)])
            return doc

    def get_dom(self, path, file_):
        file = Path(os.path.join(path, file_))
        if os.path.exists(file):
            dom = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            # dom = " ".join([str(dom.day), str(dom.month), str(dom.year)])
            dom = dom.strftime('%d %b %Y')
            return dom

    def OnSelectPrefix(self, event):
        if self.prefix_options.current() == 0:
            self.custom_prefix_entry['state'] = 'enabled'
        else:
            self.custom_prefix_entry['state'] = 'disabled'

    def OnSelectName(self, event):
        if self.fname_options.current() == 0:
            self.custom_fname_entry['state'] = 'enabled'
        else:
            self.custom_fname_entry['state'] = 'disabled'

    def OnSelectPostfix(self, event):
        if self.postfix_options.current() == 0:
            self.custom_postfix_entry['state'] = 'enabled'
        else:
            self.custom_postfix_entry['state'] = 'disabled'

    def validate_fname(self, fname):
        invalid_chars = ['/', '\\', '|', ':', '*', '?', '"', '<', '>']
        for char in fname:
            if char in invalid_chars:
                return False
        return True


    def disable_all(self):
        disable(self.top_frame)
        disable(self.entry_frame)
        disable(self.check_frame)

    def enable_all(self):
        enable(self.top_frame, 'enabled')
        enable(self.check_frame, 'readonly')
        enable(self.entry_frame, 'enabled')
