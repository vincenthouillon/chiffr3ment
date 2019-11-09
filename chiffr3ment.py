from tkinter import *
from os.path import join
from json import load


class Chiffrement:
    def __init__(self, root):
        self.get_settings()

        # region: INITIALISE WINDOW
        self.root = root
        self.root.title("chiffr3ment".upper())
        self.root.geometry(f"250x320")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG, padx=10, pady=10)
        self.root.focus_force()

        # endregion

        lbl_title = Label(self.root, text="chiffr3ment".upper() , bg=self.BG,
                          fg="white", font=("Sans Serif", 16, "bold")).pack()
        
        lbl_instruction = Label(self.root,
                                text="Cliquez pour ouvrir un fichier",
                                bg=self.BG, fg=self.FG).pack()
        
        frm_add = Frame(self.root, bg=self.ACCENT).pack(anchor="center")
        lbl_add = Label(frm_add, text="+", bg=self.ACCENT, fg=self.FG,
                        font=("Sans Serif", 100, "bold")).pack(fill="x", pady=20)

    def get_settings(self):
        """
        Récupération des paramètres dans le fichier JSON
        """
        with open(join("settings/config.json"), "r") as config:
            config = load(config)

        self.BG = config["dark"]["background"]
        self.FG = config["dark"]["foreground"]
        self.ACCENT = config["dark"]["accent_color"]


def main():
    root = Tk()
    app = Chiffrement(root)
    root.mainloop()


if __name__ == "__main__":
    main()
