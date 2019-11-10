import os
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class Crypto:

    def open_file(self, path):
        """Récupère le chemin du fichier à ouvrir et retourne le chemin, le
        nom du fichier, et le type de fichier.

        Arguments:
            path {str} -- Chemin vers le fichier.

        Returns:
            dict -- dirname, basename, extension
        """
        dirname, basename = os.path.split(path)
        extension = os.path.splitext(basename)[1]

        return {'dirname': dirname, 'basename': basename, 'extension': extension}

    def check_password(self, password, password2):
        """Vérifie la longueur du mot de passe (supérieur à 6 caractères) et
        contrôle si le mot de passe est identique à le vérification

        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Vérification du moit de passe

        Returns:
            str -- Messages d'erreur ou "pwd_ok"
        """
        if len(password) < 6:
            return "len_pwd_error"
        else:
            if password != password2:
                return "egal_pwd_error"
            else:
                return "pwd_ok"


    def generate_key_from_pwd(self, password, password2):
        """Génère une clef de chiffrement à partir d'un mot de passe.
        
        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe
        
        Returns:
            str -- Clé de chiffrement
        """
        good_password = self.check_password(password, password2)
        password_provided = good_password
        password = password_provided.encode() # Convert to type bytes
        salt = b'\xff\xb6\x9cH\xc7\xf4\x1b\x9ea%Z\xa8+\xeek\x94'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        return key

    def encrypt(self, password, password2):
        """Chiffrement d'un fichier avec d'un mot de passe.
        
        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe
        """
        b_key = self.generate_key_from_pwd(password, password2)
        key = b_key # Use one of the methods to get a key (it must be the same when decrypting)
        input_file = 'requirements.txt'
        output_file = 'requirements.encrypted'

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

    def decrypt(self, password, password2):
        """Déchiffrement du fichier avec un mot de passe.
        
        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe
        """
        b_key = self.generate_key_from_pwd(password, password2)
        key = b_key # Use one of the methods to get a key (it must be the same as used in encrypting)
        input_file = 'requirements.encrypted'
        output_file = 'test.txt'

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)


if __name__ == "__main__":
    crypto = Crypto()
    # path = input("Dir filename: ")
    # print(crypto.open_file(path))

    pwd = input('Enter password: ')
    pwd2 = input('Enter password confirmation: ')
    # print(crypto.check_password('password', 'password'))

    print(crypto.decrypt(pwd, pwd2))
