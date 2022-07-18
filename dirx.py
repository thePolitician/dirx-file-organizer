# -*- coding: utf-8 -*-
"""
DirX is a file and folder managing tool which lets you perform operations on them in bulk.
It contains 4 different tools which are displayed in 4 different tabs.
Tab 1: File Organizer - lets you organize files based on their attributes.
Tba 2: Folder Unpack - provides ease to move contents of all subdirectories into parent directory recursively.
Tab 3: Batch Rename - enabled you to rename files in bulk and with lot of naming flexibility.
Tab 4: Clear Temp - helps you clean junk files stored in user folder with one click.
"""
import tkinter as tk
from tkinter import ttk
from Frames import FileOrganizer, DirUnpack, BatchRename, ClearTemp, Encrypt
from windowsdpi import set_dpi_awareness
from pathlib import Path

# enables high dpi
set_dpi_awareness()

# Base class and root Window
class DirX(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("DirX")
        self.iconbitmap(Path(__file__).parent / "icons/dirx.ico")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)

        tabs = ttk.Notebook(self)
        organizer_tab = FileOrganizer(tabs)
        unpack_tab = DirUnpack(tabs)
        rename_tab = BatchRename(tabs)
        temp_tab = ClearTemp(tabs)
        encrypt_tab = Encrypt(tabs)
        # encrypt_tab = ttk.Frame(tabs)
        tabs.add(organizer_tab, text='File Organizer')
        tabs.add(unpack_tab, text='Unpack')
        tabs.add(rename_tab, text='Batch Rename')
        tabs.add(encrypt_tab,text="Encrypt/Decrypt")
        tabs.add(temp_tab, text='Clear Temp')
        # tabs.add(encrypt_tab, text='Encrypt/Decrypt')
        tabs.pack(expand=True, fill='both')

root = DirX()
root.mainloop()

"""
Unpack -> Bulk Move Options- Maintain directory structure
"""
