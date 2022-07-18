"""
File Organizer- Organizes files into separate folders based on-
1. Type of file
2. Extension of file
3. Date created
4. Date modified
Lets you undo your last operation.
"""
import pprint
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from pathlib import Path
import datetime
import os
import shutil
import pickle
from Frames.status import Status
from Frames.settings import Settings


# used for organizing files based on their type.
# DIRECTORIES = {
#     "HTML": [".html5", ".html", ".htm", ".xhtml"],
#     "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
#                ".heif", ".psd"],
#     "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
#                ".qt", ".mpg", ".mpeg", ".3gp"],
#     "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
#                   ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
#                   ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
#                   ".pptx"],
#     "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
#                  ".dmg", ".rar", ".xar", ".zip"],
#     "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
#               ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
#     "PLAINTEXT": [".txt", ".in", ".out"],
#     "PDF": [".pdf"],
#     "PYTHON": [".py"],
#     "XML": [".xml"],
#     "EXE": [".exe"],
#     "SHELL": [".sh"]
# }
#
# try:
#     config_file = open("config/config", "wb")
#     pickle.dump(DIRECTORIES, config_file)
#     config_file.close()
# except OSError:
#     print("Does not exist")

# file extensions mapped to their respective types
# FILE_FORMATS = dict()
# FILE_FORMATS = {file_format: directory
#                 for directory, file_formats in DIRECTORIES.items()
#                 for file_format in file_formats}


# disables all widgets inside a frame
def disable(frame):
    for child in frame.winfo_children():
        child.configure(state='disabled')


# enables all widgets inside a frame
def enable(frame, str):
    for child in frame.winfo_children():
        child.configure(state=str)


# Base class
class FileOrganizer(ttk.Frame):
    DIRECTORIES = dict()
    FILE_FORMATS = dict()

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.master = container
        # keeps count of files organized so can be used later to display number of files to undo
        self.nof = 0
        # variable to store type of organize chosen by the user
        self.organize_type = tk.StringVar()
        # stores last organized directory's path and all subdirectories created in the process for undo later
        self.undo_list = {'path': '', 'dirs': []}
        # retrieves home directory and sets desktop as default directory
        self.home_dir = (os.path.expanduser('~')) + '\\Desktop'
        # change working directory to home directory
        os.chdir(self.home_dir)
        # variable to store path of target directories on which operation will be performed
        self.path = tk.StringVar(value=self.home_dir)
        self.init_file_formats()

        self.main = ttk.Frame(self, padding=(30, 45, 0, 0))
        self.main.grid(row=0, column=0, sticky='NSEW')
        self.path_label = ttk.Label(self.main, text="Path:")
        self.path_label.grid(row=0, column=0, padx=10, sticky="W")
        self.path_entry = ttk.Entry(self.main, width=40, textvariable=self.path)
        self.path_entry.grid(row=0, column=1, padx=5, sticky="WE")
        self.select_button = ttk.Button(self.main, text="Select Folder", command=self.open_dialog)
        self.select_button.grid(row=0, column=2, sticky='W')

        self.buttons_frame = ttk.Frame(self, padding=(150, 20, 0, 0))
        self.buttons_frame.grid(row=1, column=0, sticky='NSEW')
        self.organize_button = ttk.Button(self.buttons_frame, text='Organize',
                                          command=self.start_organize)

        self.organize_button.grid(row=0, column=0)
        self.undo_button = ttk.Button(self.buttons_frame, text="Undo", state='disabled',
                                      command=self.undo_organize)
        self.undo_button.grid(row=0, column=2)

        self.organize_menu = ttk.Frame(self, padding=(30, 20, 0, 0))
        self.organize_menu.grid(row=2, column=0, sticky='NSEW')
        self.organize_by_label = ttk.Label(self.organize_menu, text='Organize By: ')
        self.organize_by_label.grid(row=0, column=0, padx=10)
        self.organize_options = ttk.Combobox(self.organize_menu, width=15, textvariable=self.organize_type,
                                             state='readonly')
        self.organize_options["values"] = ('Type of File', 'Extension of File', 'Date Created', 'Date Modified')
        self.organize_options.current(0)
        self.organize_options.grid(row=0, column=1, pady=3, sticky='W')

        self.status = Status(self)
        self.status.grid(row=3, column=0)

        self.settings_button = ttk.Button(self, text="Settings", command=self.settings)
        self.settings_button.grid()

    def start_organize(self):
        new_thread = threading.Thread(target=self.organize)
        new_thread.start()

    # decides which organize function to call based on user choice
    def organize(self):
        if self.organize_options.current() == 0:
            self.organize_by_type()
        elif self.organize_options.current() == 1:
            self.organize_by_ext()
        elif self.organize_options.current() == 2:
            self.organize_by_doc()
        elif self.organize_options.current() == 3:
            self.organize_by_dom()

    # organize files by their extension function
    def organize_by_ext(self):
        self.disable_all()
        path = self.path.get()
        if not self.cwd(path):
            return
        self.undo_list['path'] = path
        self.undo_list['dirs'].clear()
        # os.chdir(path)
        list_ = [file_ for file_ in os.listdir(path) if os.path.isfile(file_)]
        nof = len(list_)
        self.nof = nof
        self.status.set_status_label(nof)
        for file_ in list_:
            name, ext = os.path.splitext(file_)
            ext = ext[1:]

            if os.path.exists(path + '/' + ext):
                try:
                    shutil.move(path + '/' + file_, path + '/' + ext + '/' + file_)
                except:
                    pass
            else:
                dir_ = path + '/' + ext
                os.makedirs(dir_)
                self.undo_list['dirs'].append(dir_)
                try:
                    shutil.move(path + '/' + file_, dir_ + '/' + file_)
                except:
                    pass
            self.status.update_status()

        self.enable_all()

    # organize files by their date of creation
    def organize_by_dom(self):
        self.disable_all()
        path = self.path.get()
        if not self.cwd(path):
            return
        self.undo_list['path'] = path
        self.undo_list['dirs'].clear()
        # os.chdir(path)
        list_ = [file_ for file_ in os.listdir(path) if os.path.isfile(file_)]
        nof = len(list_)
        self.nof = nof
        self.status.set_status_label(nof)
        for file_ in list_:
            date_modified = self.get_dom(path, file_)

            if os.path.exists(path + '/' + date_modified):
                try:
                    shutil.move(path + '/' + file_, path + '/' + date_modified + '/' + file_)
                except:
                    pass
            else:
                dir_ = path + '/' + date_modified
                os.makedirs(dir_)
                self.undo_list['dirs'].append(dir_)
                try:
                    shutil.move(path + '/' + file_, dir_ + '/' + file_)
                except:
                    pass
            self.status.update_status()

        self.enable_all()

    # organize files by their date of last modification
    def organize_by_doc(self):
        self.disable_all()
        path = self.path.get()
        if not self.cwd(path):
            return
        self.undo_list['path'] = path
        self.undo_list['dirs'].clear()
        # os.chdir(path)
        list_ = [file_ for file_ in os.listdir(path) if os.path.isfile(file_)]
        nof = len(list_)
        self.nof = nof
        self.status.set_status_label(nof)
        for file_ in list_:
            date_created = self.get_doc(path, file_)

            if os.path.exists(path + '/' + date_created):
                try:
                    shutil.move(path + '/' + file_, path + '/' + date_created + '/' + file_)
                except:
                    pass
            else:
                dir_ = path + '/' + date_created
                os.makedirs(dir_)
                self.undo_list['dirs'].append(dir_)
                try:
                    shutil.move(path + '/' + file_, dir_ + '/' + file_)
                except:
                    pass
            self.status.update_status()

        self.enable_all()

    # organize files by their type
    def organize_by_type(self):
        self.disable_all()
        path = self.path.get()
        if not self.cwd(path):
            return
        self.undo_list['path'] = path
        self.undo_list['dirs'].clear()
        list_ = [file_ for file_ in os.listdir(path) if os.path.isfile(file_)]
        nof = len(list_)
        self.nof = 0
        self.status.set_status_label(nof)
        for entry in list_:
            file_path = Path(entry)
            _, file_format = os.path.splitext(file_path)
            file_format = file_format.lower()
            if file_format in self.FILE_FORMATS:
                directory_path = Path(self.FILE_FORMATS[file_format])
                if os.path.exists(directory_path):
                    try:
                        file_path.rename(directory_path.joinpath(file_path))
                        self.nof += 1
                    except:
                        pass
                else:
                    directory_path.mkdir()
                    self.undo_list['dirs'].append(directory_path)
                    try:
                        file_path.rename(directory_path.joinpath(file_path))
                        self.nof += 1
                    except:
                        pass
                self.status.update_status()
            else:
                directory_path = Path("OTHER")
                if os.path.exists(directory_path):
                    try:
                        file_path.rename(directory_path.joinpath(file_path))
                        self.nof += 1
                    except:
                        pass
                else:
                    directory_path.mkdir()
                    self.undo_list['dirs'].append(directory_path)
                    try:
                        file_path.rename(directory_path.joinpath(file_path))
                        self.nof += 1
                    except:
                        pass
                self.status.update_status()
        self.enable_all()

    # undo last organize operation
    def undo_organize(self):
        self.disable_all()
        if len(self.undo_list['dirs']) != 0:
            path = self.undo_list['path']
            self.status.set_status_label(self.nof)
            for dir_ in self.undo_list['dirs']:
                if os.path.exists(dir_):
                    file_list = os.listdir(dir_)
                    for afile in file_list:
                        try:
                            shutil.move(str(dir_) + '/' + afile, path)
                        except:
                            pass
                        self.status.update_status()
                    try:
                        os.rmdir(dir_)
                    except:
                        pass

            self.undo_list['dirs'].clear()
        self.enable_all()
        self.undo_button["state"] = 'disabled'

    # retrieves and returns 'date created' of a file in a specific format
    def get_doc(self, path, file_):
        file = Path(os.path.join(path, file_))
        if os.path.exists(file):
            doc = datetime.datetime.fromtimestamp(file.stat().st_ctime)
            doc = doc.strftime('%d %b %Y')
            # doc = " ".join([str(doc.day), str(doc.month), str(doc.year)])
            return doc

    # retrieves and returns 'date modified' of a file in a specific format
    def get_dom(self, path, file_):
        file = Path(os.path.join(path, file_))
        if os.path.exists(file):
            dom = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            # dom = " ".join([str(dom.day), str(dom.month), str(dom.year)])
            dom = dom.strftime('%d %b %Y')
            return dom

    # function to choose parent directory
    def open_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            # os.chdir(folder_path)
            self.path.set(folder_path)
        elif not self.path.get():
            self.path.set(self.home_dir)

    # change working directory
    def cwd(self, path):
        try:
            self.status.set_error_status("")
            os.chdir(path)
            return True
        except FileNotFoundError:
            self.enable_all()
            self.undo_button["state"] = 'disabled'
            self.status.set_error_status("     Invalid Path!")
            return False

    def settings(self):
        Settings(self.master)

    def load_categories(self):
        config_file = Path(__file__).parent / "../config/config"
        try:
            with open(config_file, "rb") as file:
                self.DIRECTORIES = pickle.load(file)
        except OSError:
            messagebox.showerror("Error!", "Config file not found!")

    def init_file_formats(self):
        self.load_categories()
        self.FILE_FORMATS = {file_format: directory
                             for directory, file_formats in self.DIRECTORIES.items()
                             for file_format in file_formats}

    # utility function to disable all widgets on screen
    def disable_all(self):
        disable(self.main)
        disable(self.buttons_frame)
        disable(self.organize_menu)

    # utility function to enabled all widgets on screen
    def enable_all(self):
        enable(self.main, 'enabled')
        enable(self.buttons_frame, 'enabled')
        enable(self.organize_menu, 'readonly')
