from os import system, chdir, listdir
from json import dump

def check():
    try:
        chdir("settings")

    except:
        system("mkdir settings")
        chdir("settings")

    if "themes.json" not in listdir("."):
        theme = {
            "dark": {
                "background": "#303032",
                "accent_color": "#F4B444",
                "foreground": "#DFDFE0"
            }
        }

        with open("themes.json", "w") as write:
            dump(theme, write, indent=4)

    if "languages.json" not in listdir("."):
        language = {
            "fr": {
                "instruction": "Cliquez pour ouvrir un fichier",
                "password": "Mot de passe",
                "confirm": "Confirmation",
                "checkbox_show_password": "Voir mot de passe",
                "button_cancel": "Annuler",
                "button_encrypt": "Chiffrer",
                "button_decrypt":"Déchiffrer",
                "title_openfile": "Choisir un fichier",
                "title_window_error": "Erreur",
                "title_window_success": "Succès",
                "msg_error_file": "Veuillez choisir un fichier",
                "msg_error_length_pwd": "Veuillez saisir un mot de passe d'au moins 6 caractères",
                "msg_error_egal_pwd": "Les mots de passe ne sont pas identique",
                "msg_success_encrypt": "Votre fichier a bien été chiffré",
                "msg_success_decrypt": "Votre fichier a bien été déchiffré",
                "msg_error_pwd": "Mot de passe incorrect"
            }
        }

        with open("languages.json", "w") as write:
            dump(language, write, indent=4)
    
    if "config.json" not in listdir("."):
        settings = {
            "settings": {
                "theme": "dark",
                "language": "fr"
            }
        }

        with open("config.json", "w") as write:
            dump(settings, write, indent=4)