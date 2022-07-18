import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from tkinter import simpledialog


class Settings:
    DIRECTORIES = dict()

    def __init__(self, master, *args, **kwargs):
        self.list_var = tk.StringVar()
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.grab_set()
        self.top.title("Settings")
        self.top.iconbitmap(Path(__file__).parent / "../icons/dirx.ico")
        self.top.geometry('600x400')
        self.top.resizable(False, False)
        self.init_directories()
        self.top_frame = ttk.Frame(self.top, padding=(10, 10, 0, 10))
        self.top_frame.grid(row=0, column=0, sticky='NEW')

        self.group_list = tk.Listbox(self.top_frame, listvariable=self.list_var, font=("TkDefaultFont", 9), height=10, selectmode='single',
                                     activestyle='none')
        self.group_list.bind("<<ListboxSelect>>", self.OnSelect)
        self.group_list.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)

        self.cat_scroll = ttk.Scrollbar(self.top_frame, orient='vertical', command=self.group_list.yview)
        self.cat_scroll.grid(row=0, column=1, sticky='nsw')
        self.group_list['yscrollcommand'] = self.cat_scroll.set

        self.text_frame = ttk.Frame(self.top_frame, padding=5)
        self.text_frame.grid(row=0, column=2, sticky='NSEW')

        self.button_frame = ttk.Frame(self.text_frame, padding=2)
        self.button_frame.grid(row=1, column=0, sticky='NSEW')

        self.ext_field = tk.Text(self.text_frame, width=35, height=8, wrap='word', state='disabled')
        self.ext_field.grid(row=0, column=0, sticky='n', padx=5, pady=5)

        self.ext_scroll = ttk.Scrollbar(self.text_frame, orient='vertical', command=self.ext_field.yview)
        self.ext_scroll.grid(row=0, column=1, sticky='nsw')
        self.ext_field['yscrollcommand'] = self.ext_scroll.set

        self.fill_list()
        self.fill_ext_field()

        self.botframe = ttk.Frame(self.top, padding=10)
        self.botframe.grid(row=1, column=0, sticky='SEW')

        self.new_group_button = ttk.Button(self.botframe, text="New Group", command=self.new_group)
        self.new_group_button.grid(row=0, column=0)

        self.apply_button = ttk.Button(self.button_frame, text="Apply", state='disabled', command=self.apply_changes)
        self.apply_button.grid(row=0, column=0)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", state='disabled', command=self.cancel_changes)
        self.cancel_button.grid(row=0, column=1)

        self.edit_button = ttk.Button(self.botframe, text='Edit', command=self.edit_group)
        self.edit_button.grid(row=0, column=1)

        self.remove_button = ttk.Button(self.botframe, text="Remove", command=self.remove_group)
        self.remove_button.grid(row=0, column=2)

    def OnSelect(self, event):
        self.apply_button['state'] = 'disabled'
        self.cancel_button['state'] = 'disabled'
        self.fill_ext_field()

    def fill_ext_field(self):
        self.clear_field()
        if self.group_list.size() > 0:
            self.ext_field['state'] = 'normal'
            selected_category = self.group_list.get(self.group_list.curselection()[0])
            if selected_category in self.DIRECTORIES.keys():
                ext_string = "; ".join(self.DIRECTORIES[selected_category])
                self.ext_field.insert('1.0', ext_string)
            self.ext_field['state'] = 'disabled'

    def fill_list(self):
        index = 0
        for entry in self.DIRECTORIES.keys():
            self.group_list.insert(index, entry)
            index += 1
        self.clear_selection()
        self.group_list.select_set(0)

    def new_group(self):
        new_group = simpledialog.askstring("New", "Group Name", parent=self.top)
        if new_group is not None:
            self.group_list.insert('end', new_group)
            index = self.group_list.size()-1
            self.clear_selection()
            self.group_list.select_set(index)
            self.group_list.see(index)
            self.clear_field()
            self.ext_field['state'] = 'normal'
            self.apply_button['state'] = 'enabled'
            self.cancel_button['state'] = 'enabled'

    def edit_group(self):
        self.apply_button['state'] = 'enabled'
        self.cancel_button['state'] = 'enabled'
        self.ext_field['state'] = 'normal'

    def remove_group(self):
        group_id = self.group_list.curselection()[0]
        group_name = self.group_list.get(group_id)
        self.group_list.delete(group_id)
        del self.DIRECTORIES[group_name]
        self.update_config()
        self.init_directories()
        if group_id > 0:
            self.clear_selection()
            self.group_list.select_set(group_id - 1)
        elif group_id == 0 and self.group_list.size() > 0:
            self.clear_selection()
            self.group_list.select_set(group_id)
        self.fill_ext_field()

    def clear_field(self):
        self.ext_field['state'] = 'normal'
        self.ext_field.delete('1.0', 'end')
        self.ext_field['state'] = 'disabled'

    def apply_changes(self):
        ext_str = self.ext_field.get('1.0', 'end')
        if ext_str != "":
            ext_list = self.parse_ext(ext_str)
            if self.validate_ext(ext_list):
                group = self.group_list.get(self.group_list.curselection())
                self.DIRECTORIES[group] = ext_list
                # print(self.DIRECTORIES[group])
                self.update_config()
                self.init_directories()
            else:
                messagebox.showerror("Error!", "Invalid extension format!")
                self.fill_ext_field()
            # print(self.DIRECTORIES.keys())
        self.ext_field['state'] = 'disabled'
        self.apply_button['state'] = 'disabled'
        self.cancel_button['state'] = 'disabled'

    def cancel_changes(self):
        self.fill_ext_field()
        self.apply_button['state'] = 'disabled'
        self.cancel_button['state'] = 'disabled'

    def parse_ext(self, ext_str):
        ext_list = [ext.strip() for ext in ext_str.split(';')]
        return ext_list

    def validate_ext(self, ext_list):
        for ext in ext_list:
            if ext[0] != '.':
                return False
            else:
                invalid_chars = ['/','\\', ':', '*', '?', '"', '<', '>', '|']
                for char in ext:
                    if char in invalid_chars:
                        return False
        return True

    def clear_selection(self):
        if self.group_list.curselection():
            self.group_list.select_clear(*self.group_list.curselection())

    def init_directories(self):
        config_file = Path(__file__).parent / "../config/config"
        try:
            with open(config_file, "rb") as file:
                self.DIRECTORIES = pickle.load(file)
        except OSError:
            messagebox.showerror("Error!", "Config file not found!")

    def update_config(self):
        config_file = Path(__file__).parent / "../config/config"
        try:
            with open(config_file, "wb") as file:
                pickle.dump(self.DIRECTORIES, file)
        except OSError:
            messagebox.showerror("Error!", "Config file not found!")
