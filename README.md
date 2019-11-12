# chiffr3ment

Chiffrer et déchiffrer vos fichiers en quelques clics avec chiffr3ment. Compatible Windows, MacOS & Ubuntu.

![screenshot](screenshot.png)

---

## Table des matières
- [Introduction](#Description)
- [Technologies](#Technologies)
- [Plateformes](#Plateformes)
- [Installation](#Installation)
- [Auteurs](#Auteurs)

## Description
Ce programme écrit en Python vous permet de chiffrer/dechiffrer vos fichiers.

Chiffr3ment est multilingue (languages.json) et personnalisable (themes.json), l'activation des paramètres se font via le fichier 'config.json'.

## Technologies
Programme écrit avec :
- Python >= 3.6
- [cryptography](https://cryptography.io/en/latest/)==2.8
 

## Plateformes
- Windows (testé sur Windows 10)
- MacOS (testé sur MacOS Catalina)
- Linux (testé sur Ubuntu 19)

## Installation

```
$ python3 -m venv venv
$ venv\Scripts\activate.bat 'ou source venv/bin/activate'
$ pip install -r requirements.txt
$ python3 chiffr3ment.py
```

## Auteurs
- Vincent Houillon
- Quentin Houillon
