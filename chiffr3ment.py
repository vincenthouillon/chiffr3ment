from json import load
from os import chdir, getcwd, name
from os.path import basename, dirname, getsize, join, splitext
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo

from core.check_settings import *
from core.crypto import *


class Chiffrement:
    def __init__(self, root):
        chdir(dirname(getcwd()))

        self.get_settings()
        self.crypt = Crypto()

        # region: INITIALISE WINDOW
        self.root = root
        self.root.title("chiffr3ment".upper())
        self.root.geometry(f"250x290")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG, padx=10, pady=10)
        self.icones()
        self.root.focus_force()
        # endregion: INITIALISE WINDOW

        # region: FRAME
        self.frm_add = Frame(self.root, bg=self.ACCENT)
        self.frm_encrypt = Frame(self.root, bg=self.ACCENT)
        self.frm_decrypt = Frame(self.root, bg=self.ACCENT)
        self.frm_config = Frame(self.root, bg=self.BG)
        # endregion: FRAME

        # region: IMAGE
        self.theme = PhotoImage(file="theme.png")
        self.language = PhotoImage(file="language.png")
        # endregion; IMAGE

        # region: LABEL
        self.lbl_title = Label(self.root, text="chiffr3ment".upper(),
                               bg=self.BG, fg="white",
                               font=("Sans Serif", 11, "bold"))

        self.lbl_instruction = Label(self.root,
                                     text=self.MY_LANGUAGE[self.LANGUAGE]["instruction"],
                                     bg=self.BG, fg=self.FG)
        

        self.lbl_add = Label(self.frm_add, text="+", bg=self.ACCENT, fg=self.BG,
                             font=("Sans Serif", 75, "bold"))

        self.lbl_encrypt_pwd = Label(self.frm_encrypt,
                                     text=self.MY_LANGUAGE[self.LANGUAGE]["password"],
                                     bg=self.ACCENT, fg=self.BG,
                                     font=("Sans Serif", 7), anchor="w")

        self.lbl_encrypt_confirm = Label(self.frm_encrypt,
                                         text=self.MY_LANGUAGE[self.LANGUAGE]["confirm"],
                                         bg=self.ACCENT, fg=self.BG,
                                         font=("Sans Serif", 7), anchor="w")

        self.lbl_decrypt_pwd = Label(self.frm_decrypt,
                                     text=self.MY_LANGUAGE[self.LANGUAGE]["password"],
                                     bg=self.ACCENT, fg=self.BG,
                                     font=("Sans Serif", 7), anchor="w")
        
        self.lbl_theme = Label(self.frm_config, image=self.theme, bg=self.BG)

        self.lbl_language = Label(self.frm_config, image=self.language,
                                  bg=self.BG)

        self.lbl_add.bind("<ButtonRelease-1>", self.open_file)
        self.lbl_theme.bind("<ButtonRelease-1>", self.theme_configuration)
        self.lbl_language.bind("<ButtonRelease-1>", self.language_configuration)
        # endregion: LABEL

        # region: ENTRY
        self.ent_encrypt_pwd = Entry(self.frm_encrypt, bg=self.ACCENT,
                                     fg=self.BG, show="*", justify="center",
                                     highlightthickness=0, bd=0,
                                     font=("Sans Serif", 11, "bold"))

        self.ent_encrypt_confirm = Entry(self.frm_encrypt, bg=self.ACCENT,
                                         fg=self.BG, show="*", justify="center",
                                         highlightthickness=0, bd=0,
                                         font=("Sans Serif", 11, "bold"))

        self.ent_decrypt_pwd = Entry(self.frm_decrypt, bg=self.ACCENT,
                                     fg=self.BG, show="*", justify="center",
                                     highlightthickness=0, bd=0,
                                     font=("Sans Serif", 11, "bold"))

        self.ent_encrypt_pwd.focus()
        self.ent_decrypt_pwd.focus()
        self.ent_encrypt_pwd.bind("<Return>", self.focus_entry)
        self.ent_encrypt_confirm.bind("<Return>", self.ent_encrypt)
        self.ent_decrypt_pwd.bind("<Return>", self.ent_decrypt)
        # endregion: ENTRY

        # region: CHECKBUTTON
        self.ckb_show_pwd_encrypt = Checkbutton(self.frm_encrypt,
                                                text=self.MY_LANGUAGE[self.LANGUAGE]
                                                ["checkbox_show_password"],
                                                bg=self.ACCENT, fg=self.BG,
                                                font=("Sans Serif", 7),
                                                anchor="w", relief="flat",
                                                highlightbackground=self.ACCENT,
                                                activebackground=self.ACCENT,
                                                command=self.show_pwd_encrypt)

        self.ckb_show_pwd_decrypt = Checkbutton(self.frm_decrypt,
                                                text=self.MY_LANGUAGE[self.LANGUAGE]
                                                ["checkbox_show_password"],
                                                bg=self.ACCENT, fg=self.BG,
                                                font=("Sans Serif", 7),
                                                anchor="w", relief="flat",
                                                highlightbackground=self.ACCENT,
                                                activebackground=self.ACCENT,
                                                command=self.show_pwd_decrypt)
        # endregion: CHECKBUTTON

        # region: BUTTON
        self.btn_run = Button(fg="black", relief="flat",
                              highlightbackground=self.BG)

        self.btn_cancel = Button(text=self.MY_LANGUAGE[self.LANGUAGE]["button_cancel"],
                                 fg="black", relief="flat",
                                 command=self.cancel,
                                 highlightbackground=self.BG)
        # endregion: BUTTON

        # region: PACK
        self.lbl_title.pack(anchor="center")
        self.lbl_instruction.pack()

        self.lbl_add.pack(fill="x")
        self.frm_add.pack(anchor="center", fill="x", pady=15)

        self.lbl_encrypt_pwd.pack(fill="x", pady=3)
        self.ent_encrypt_pwd.pack(fill="x", ipady=2)
        self.lbl_encrypt_confirm.pack(fill="x", pady=3)
        self.ent_encrypt_confirm.pack(fill="x", ipady=2)
        self.ckb_show_pwd_encrypt.pack(fill="x")

        self.lbl_decrypt_pwd.pack(fill="x", pady=3)
        self.ent_decrypt_pwd.pack(fill="x", ipady=2)
        self.ckb_show_pwd_decrypt.pack(fill="x")

        self.lbl_theme.pack(side="right", padx=2)
        self.lbl_language.pack(side="right", padx=2)
        self.frm_config.pack(side="bottom", anchor="w")
        # endregion: PACK

    def get_settings(self):
        """
        Retrieving parameters in the JSON file
        """
        with open("settings/config.json", "r") as config:
            self.SETTING = load(config)

        with open("settings/themes.json", "r") as theme:
            self.MY_THEME = load(theme)

        with open("settings/languages.json", "r") as language:
            self.MY_LANGUAGE = load(language)

        self.THEME = self.SETTING["settings"]["theme"]
        self.LANGUAGE = self.SETTING["settings"]["language"]

        self.BG = self.MY_THEME[self.THEME]["background"]
        self.FG = self.MY_THEME[self.THEME]["foreground"]
        self.ACCENT = self.MY_THEME[self.THEME]["accent_color"]

    def icones(self):
        """
        Displays the icon according to the operating system
        """
        if "nt" == name:
            self.root.iconbitmap("icons/icon.ico")
        else:
            img = Image("photo", file="icons/icon.png")
            self.root.tk.call("wm", "iconphoto", self.root._w, img)

    def show_pwd_encrypt(self):
        """
        Show or hide the password of the frame 'encrypt'
        """
        if self.ent_encrypt_pwd["show"] == "*":
            self.ent_encrypt_pwd["show"] = ""
            self.ent_encrypt_confirm["show"] = ""
        else:
            self.ent_encrypt_pwd["show"] = "*"
            self.ent_encrypt_confirm["show"] = "*"

    def show_pwd_decrypt(self):
        """
        Show or hide the password of the frame 'decrypt'
        """
        if self.ent_decrypt_pwd["show"] == "*":
            self.ent_decrypt_pwd["show"] = ""
        else:
            self.ent_decrypt_pwd["show"] = "*"

    def show_encrypt_decrypt(self):
        self.frm_add.pack_forget()

        extension = splitext(self.file.name)[1]
        if extension == ".ch3":
            self.btn_run.config(text=self.MY_LANGUAGE[self.LANGUAGE]["button_decrypt"],
                                command=self.decrypt)

            self.frm_decrypt.pack(fill="x", pady=15, anchor="n")
        else:
            self.btn_run.config(text=self.MY_LANGUAGE[self.LANGUAGE]["button_encrypt"],
                                command=self.encrypt)

            self.frm_encrypt.pack(fill="x", pady=15, anchor="n")

        self.btn_run.pack(side="right", anchor="s", pady=10, ipadx=4)
        self.btn_cancel.pack(side="right", anchor="s", padx=20, pady=10,
                             ipadx=4)

        file_name = basename(self.file.name)
        size_name = getsize(self.file.name)/1024

        # Truncate the file name if it is too long...
        if len(file_name) > 23:
            self.lbl_instruction.config(
                text=f"{file_name[0:20]:.<23} - {size_name:.2f} MB")
        else:
            self.lbl_instruction.config(
                text=f"{file_name} - {size_name:.2f} MB")

    def open_file(self, event):
        try:
            self.file = filedialog.askopenfile(
                title=self.MY_LANGUAGE[self.LANGUAGE]["title_openfile"])

            self.show_encrypt_decrypt()
        except:
            self.cancel()
            showerror(self.MY_LANGUAGE[self.LANGUAGE]["title_window_error"],
                      self.MY_LANGUAGE[self.LANGUAGE]["msg_error_file"])

    def focus_entry(self, event):
        self.ent_encrypt_confirm.focus()

    def cancel(self):
        """
        Window refresh
        """
        self.frm_encrypt.pack_forget()
        self.frm_decrypt.pack_forget()

        self.btn_run.pack_forget()
        self.btn_cancel.pack_forget()

        self.ent_encrypt_pwd.delete(0, END)
        self.ent_encrypt_confirm.delete(0, END)
        self.ent_decrypt_pwd.delete(0, END)
        self.lbl_instruction.config(
            text=self.MY_LANGUAGE[self.LANGUAGE]["instruction"])

        self.frm_add.pack(anchor="center", fill="x", pady=15)

    def encrypt(self):
        pwd = self.ent_encrypt_pwd.get()
        confirm = self.ent_encrypt_confirm.get()

        function_encrypted = self.crypt.encrypt(self.file.name, pwd, confirm)

        if function_encrypted == "len_pwd_error":
            showerror(self.MY_LANGUAGE[self.LANGUAGE]["title_window_error"],
                      self.MY_LANGUAGE[self.LANGUAGE]["msg_error_length_pwd"])
        elif function_encrypted == "egal_pwd_error":
            showerror(self.MY_LANGUAGE[self.LANGUAGE]["title_window_error"],
                      self.MY_LANGUAGE[self.LANGUAGE]["msg_error_egal_pwd"])
        else:
            showinfo(self.MY_LANGUAGE[self.LANGUAGE]["title_window_success"],
                     self.MY_LANGUAGE[self.LANGUAGE]["msg_success_encrypt"])

            self.cancel()

    def decrypt(self):
        pwd = self.ent_decrypt_pwd.get()
        function_decrypted = self.crypt.decrypt(self.file.name, pwd)

        if function_decrypted == "incorrect_pwd":
            showerror(self.MY_LANGUAGE[self.LANGUAGE]["title_window_error"],
                      self.MY_LANGUAGE[self.LANGUAGE]["msg_error_pwd"])
        else:
            showinfo(self.MY_LANGUAGE[self.LANGUAGE]["title_window_success"],
                     self.MY_LANGUAGE[self.LANGUAGE]["msg_success_decrypt"])

            self.cancel()
    
    def window_configuration(self, sett):
        #region: TOPLEVEL
        window_config = Toplevel(bg=self.BG)
        window_config.resizable(False, False)
        window_config.focus_force()
        # endregion: TOPLEVEL

        # region: LISTBOX
        self.lsb = Listbox(window_config, bg=self.BG, fg=self.ACCENT,
                           highlightbackground=self.BG, highlightcolor=self.BG,
                           bd=0)
        
        self.lsb.bind("<<ListboxSelect>>", lambda x: self.handler(sett))
        # endregion: LISTBOX

        self.display_configuration(sett)

        window_config.mainloop()
    
    def display_configuration(self, sett):
        for n, i in enumerate(sett, start=1):
            self.lsb.insert(n, i)
            self.lsb.pack()
    
    def handler(self, sett):
        select = self.lsb.curselection()
        new_setting = self.lsb.get(select)

        if sett == self.MY_THEME:
            self.SETTING["settings"]["theme"] = new_setting
        
        else:
            self.SETTING["settings"]["language"] = new_setting

        with open("settings/config.json", "w") as settings:
            dump(self.SETTING, settings, indent=4)

        self.root.destroy()
        main()

    def theme_configuration(self, event):
        self.window_configuration(self.MY_THEME)
    
    def language_configuration(self, event):
        self.window_configuration(self.MY_LANGUAGE)

    def ent_encrypt(self, event):
        self.encrypt()

    def ent_decrypt(self, event):
        self.decrypt()


def main():
    check()
    root = Tk()
    app = Chiffrement(root)
    root.mainloop()


if __name__ == "__main__":
    main()
