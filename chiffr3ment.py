from json import load
from os.path import basename, getsize, join, splitext
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo

from core.crypto import *

THEME = "dark"


class Chiffrement:
    def __init__(self, root):
        self.get_settings()
        self.crypt = Crypto()

        # region: INITIALISE WINDOW
        self.root = root
        self.root.title("chiffr3ment".upper())
        self.root.geometry(f"250x285")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG, padx=10, pady=10)
        self.root.focus_force()

        # endregion: INITIALISE WINDOW

        # region: FRAME
        self.frm_add = Frame(self.root, bg=self.ACCENT)
        self.frm_encrypt = Frame(self.root, bg=self.ACCENT)
        self.frm_decrypt = Frame(self.root, bg=self.ACCENT)

        # endregion: FRAME

        # region: LABEL
        self.lbl_title = Label(self.root, text="chiffr3ment".upper(),
                               bg=self.BG, fg="white",
                               font=("Sans Serif", 11, "bold"))

        self.lbl_instruction = Label(self.root,
                                     text="Cliquez pour ouvrir un fichier",
                                     bg=self.BG, fg=self.FG)

        self.lbl_add = Label(self.frm_add, text="+", bg=self.ACCENT, fg=self.BG,
                             font=("Sans Serif", 75, "bold"))

        self.lbl_encrypt_pwd = Label(self.frm_encrypt, text="Mot de passe",
                                     bg=self.ACCENT, fg=self.BG,
                                     font=("Sans Serif", 7), anchor="w")

        self.lbl_encrypt_confirm = Label(self.frm_encrypt, text="Confirmation",
                                         bg=self.ACCENT, fg=self.BG,
                                         font=("Sans Serif", 7), anchor="w")

        self.lbl_decrypt_pwd = Label(self.frm_decrypt, text="Mot de passe",
                                     bg=self.ACCENT, fg=self.BG,
                                     font=("Sans Serif", 7), anchor="w")

        self.lbl_add.bind("<ButtonRelease-1>", self.open_file)

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
                                                text="Voir mots de passe",
                                                bg=self.ACCENT, fg=self.BG,
                                                font=("Sans Serif", 7),
                                                anchor="w", relief="flat",
                                                command=self.show_pwd_encrypt)

        self.ckb_show_pwd_decrypt = Checkbutton(self.frm_decrypt,
                                                text="Voir mot de passe",
                                                bg=self.ACCENT, fg=self.BG,
                                                font=("Sans Serif", 7),
                                                anchor="w", relief="flat",
                                                command=self.show_pwd_decrypt)

        # endregion: CHECKBUTTON

        # region: BUTTON
        self.btn_run = Button(fg="black", relief="flat", 
                              highlightbackground=self.BG)

        self.btn_cancel = Button(text="Annuler", fg="black", relief="flat",
                                 command=self.cancel,
                                 highlightbackground=self.BG)

        # endregion: BUTTON

        # region: PACK
        self.lbl_title.pack()
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

        # endregion: PACK

    def get_settings(self):
        """
        Récupération des paramètres dans le fichier JSON
        """
        with open(join("settings/config.json"), "r") as config:
            config = load(config)

        self.BG = config[THEME]["background"]
        self.FG = config[THEME]["foreground"]
        self.ACCENT = config[THEME]["accent_color"]

    def show_pwd_encrypt(self):
        """
        Afficher ou masquer le mot de passe de la frame "encrypt"
        """
        if self.ent_encrypt_pwd["show"] == "*":
            self.ent_encrypt_pwd["show"] = ""
            self.ent_encrypt_confirm["show"] = ""

        else:
            self.ent_encrypt_pwd["show"] = "*"
            self.ent_encrypt_confirm["show"] = "*"

    def show_pwd_decrypt(self):
        """
        Afficher ou masquer le mot de passe de la frame "decrypt"
        """
        if self.ent_decrypt_pwd["show"] == "*":
            self.ent_decrypt_pwd["show"] = ""

        else:
            self.ent_decrypt_pwd["show"] = "*"

    def show_encrypt_decrypt(self):
        self.frm_add.pack_forget()

        extension = splitext(self.file.name)[1]
        if extension == ".ch3":
            self.btn_run.config(text="Dechiffrer", command=self.decrypt)
            self.frm_decrypt.pack(fill="x", pady=15, anchor="n")

        else:
            self.btn_run.config(text="Chiffrer", command=self.encrypt)
            self.frm_encrypt.pack(fill="x", pady=15, anchor="n")

        self.btn_run.pack(side="right", anchor="s", pady=10, ipadx=4)
        self.btn_cancel.pack(side="right", anchor="s", padx=20, pady=10,
                             ipadx=4)

        file_name = basename(self.file.name)
        size_name = getsize(self.file.name)/1024

        self.lbl_instruction.config(text=f"{file_name} - {size_name:.2f} MB")

    def open_file(self, event):
        try:
            self.file = filedialog.askopenfile(title="Choisir un fichier")
            self.show_encrypt_decrypt()

        except:
            self.cancel()
            showerror("Erreur", "Veuillez choisir un fichier !!!")

    def focus_entry(self, event):
        self.ent_encrypt_confirm.focus()

    def cancel(self):
        """
        rafraîchissement de la fenêtre
        """
        self.frm_encrypt.pack_forget()
        self.frm_decrypt.pack_forget()

        self.btn_run.pack_forget()
        self.btn_cancel.pack_forget()

        self.ent_encrypt_pwd.delete(0, END)
        self.ent_encrypt_confirm.delete(0, END)
        self.ent_decrypt_pwd.delete(0, END)

        self.frm_add.pack(anchor="center", fill="x", pady=15)

    def encrypt(self):
        pwd = self.ent_encrypt_pwd.get()
        confirm = self.ent_encrypt_confirm.get()

        function_encrypted = self.crypt.encrypt(self.file.name, pwd, confirm)

        if function_encrypted == "len_pwd_error":
            showerror("Erreur",
                      "Veuillez saisir un mot de passe d'au moins 6 caractères")

        elif function_encrypted == "egal_pwd_error":
            showerror("Erreur", "Les mots de passe ne sont pas identique")

        else:
            showinfo("Succès", "Votre fichier a bien été chiffré")
            self.cancel()

    def decrypt(self):
        pwd = self.ent_decrypt_pwd.get()
        function_decrypted = self.crypt.decrypt(self.file.name, pwd)

        if function_decrypted == "incorrect_pwd":
            showerror("Erreur", "Mot de passe incorrect")

        else:
            showinfo("Succès", "Votre fichier a bien été déchiffré")
            self.cancel()

    def ent_encrypt(self, event):
        self.encrypt()

    def ent_decrypt(self, event):
        self.decrypt()


def main():
    root = Tk()
    app = Chiffrement(root)
    root.mainloop()


if __name__ == "__main__":
    main()
