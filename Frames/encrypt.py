import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


class Encrypt(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.path = tk.StringVar(value="")
        self.enc_status = tk.StringVar()
        self.head = "aes_encrypted_file".encode('utf-8')
        self.main = ttk.Frame(self, padding=(30, 45, 0, 0))
        self.main.grid(row=0, column=0, sticky='NSEW')
        self.path_label = ttk.Label(self.main, text="Path:")
        self.path_label.grid(row=0, column=0, padx=10, sticky="W")
        self.path_entry = ttk.Entry(self.main, width=40, textvariable=self.path)
        self.path_entry.grid(row=0, column=1, padx=5, sticky="WE")
        self.select_button = ttk.Button(self.main, text="Select File", command=self.open_dialog)
        self.select_button.grid(row=0, column=2, sticky='W')

        self.button_frame = ttk.Frame(self.main)
        self.button_frame.grid(row=1, column=1, sticky='nsew')

        self.encrypt_button = ttk.Button(self.button_frame, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.grid(row=0, column=0, sticky='ew', pady=10)

        self.decrypt_button = ttk.Button(self.button_frame, text="Decrypt", command=self.decrypt_file)
        self.decrypt_button.grid(row=0, column=1, sticky='ew', pady=10)

        style = ttk.Style(self)
        style.configure('Green.TLabel', foreground='green')
        self.status = ttk.Label(self.main, text="", textvariable=self.enc_status, style='Green.TLabel')
        self.status.grid(row=2, column=0, sticky="nsew")

    def encrypt_file(self):
        self.disable_all()
        self.enc_status.set("")
        if self.path.get() == "":
            self.enable_all()
            return
        # path = Path(os.path.dirname(self.path.get()))
        # if path.exists():
        #     os.chdir(path)
        # else:
        #     messagebox.showerror("Error!", "Invalid Path!")
        #     return
        if not self.check_encryption():
            password = self.get_password()
            if password is not None:
                self.encrypt(self.getKey(password))
                self.enc_status.set("Success!")
        else:
            messagebox.showerror("Error!", "File is already encrypted")
        self.enable_all()
        return

    def decrypt_file(self):
        self.disable_all()
        self.enc_status.set("")
        if self.path.get() == "":
            self.enable_all()
            return
        # path = Path(os.path.dirname(self.path.get()))
        # if path.exists():
        #     os.chdir(path)
        # else:
        #     messagebox.showerror("Error!", "Invalid Path!")
        #     return
        try:
            if self.check_encryption():
                password = simpledialog.askstring("Password", "Password to Decrypt:", parent=self)
                if password is not None:
                    key = self.getKey(password)
                    if self.check_hash(key):
                        self.decrypt(key)
                        self.enc_status.set("Success!")
                    else:
                        messagebox.showerror("Error!", "Incorrect Password!")
            else:
                messagebox.showerror("Error!", "File is not encrypted")
        except FileNotFoundError:
            messagebox.showerror("Error!", "File not found!")
        except ValueError as e:
            messagebox.showerror("Error!", e.args[0])
        self.enable_all()
        return

    def check_encryption(self):
        file = self.path.get()
        try:
            with open(file, 'rb') as infile:
                data = infile.read(len(self.head))
                if data == self.head:
                    return True
            return False
        except FileNotFoundError:
            raise FileNotFoundError
        except:
            raise ValueError("Unknown error occurred!")

    def check_hash(self, key):
        file = self.path.get()
        try:
            with open(file, 'rb') as infile:
                infile.seek(len(self.head))
                hash_len = int(infile.read(16))
                if hash_len != len(key):
                    return False
                hash = infile.read(hash_len)
                if hash == key:
                    return True
                else:
                    return False
        except FileNotFoundError:
            raise FileNotFoundError
        except:
            raise ValueError("Unknown error occurred!")

    # def check_decryption(self, key):
    #     file = self.path.get()
    #     if self.check_encryption():
    #         with open(file, 'rb') as infile:
    #             infile.seek(len(self.head))
    #             hash_len = int(infile.read(16))
    #             hash = infile.read(hash_len)
    #             if hash == key:
    #                 return True
    #             else:
    #                 messagebox.showerror("Error!", "Incorrect Password!")
    #     else:
    #         messagebox.showerror("Error!", "File is not encrypted")
    #     return False

    def encrypt(self, key):
        chunksize = 64 * 1024
        filename = self.path.get()
        outputFile = os.path.join(os.path.dirname(filename), os.path.basename(filename)+".enc")
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)
        hash_len = str(len(key)).zfill(16)
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        try:
            with open(filename, 'rb') as infile:
                with open(outputFile, 'wb') as outfile:
                    outfile.write(self.head)
                    outfile.write(hash_len.encode('utf-8'))
                    outfile.write(key)
                    outfile.write(filesize.encode('utf-8'))
                    outfile.write(IV)

                    while True:
                        chunk = infile.read(chunksize)

                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += b' ' * (16 - (len(chunk) % 16))

                        outfile.write(encryptor.encrypt(chunk))
        except FileNotFoundError:
            messagebox.showerror("Error!", "File not found!")
        except:
            messagebox.showerror("Error!", "Unknown error occurred!")

    def decrypt(self, key):
        chunksize = 64 * 1024
        filename = self.path.get()
        file = os.path.basename(filename)
        if Path(file).suffix == ".enc":
            file = os.path.splitext(file)[0]
        outputFile = os.path.join(os.path.dirname(filename), "(decrypted)"+file)
        seek_pos = len(self.head) + 16 + len(key)

        try:
            with open(filename, 'rb') as infile:
                infile.seek(seek_pos)
                filesize = int(infile.read(16))
                IV = infile.read(16)

                decryptor = AES.new(key, AES.MODE_CBC, IV)

                with open(outputFile, 'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize)

                        if len(chunk) == 0:
                            break

                        outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)
        except FileNotFoundError:
            messagebox.showerror("Error!", "File not found!")
        except:
            messagebox.showerror("Error!", "Unknown error occurred!")

    def getKey(self, password):
        hasher = SHA256.new(password.encode('utf-8'))
        return hasher.digest()

    def get_password(self):
        password = None
        while password is None:
            passwd = simpledialog.askstring("Password", "Password to Encrypt:", parent=self)
            if passwd is None:
                break
            password = passwd
            if password is not None:
                if len(password)<7:
                    messagebox.showerror("Too Short", "Minimum length of password is 6. Please try again.")
                    password = None
                elif len(password)>16:
                    messagebox.showerror("Too Long", "Maximum length of password is 16. Please try again.")
                    password = None
        return password

    def disable_all(self):
        self.path_label['state'] = 'disabled'
        self.select_button['state'] = 'disabled'
        self.encrypt_button['state'] = 'disabled'
        self.decrypt_button['state'] = 'disabled'

    def enable_all(self):
        self.path_label['state'] = 'enabled'
        self.select_button['state'] = 'enabled'
        self.encrypt_button['state'] = 'enabled'
        self.decrypt_button['state'] = 'enabled'

    def open_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path.set(file_path)
