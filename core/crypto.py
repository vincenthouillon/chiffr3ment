import os
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class Crypto:
    """Chiffrement déchiffrement de fichiers.

    Utilisation:
        Crypto.encrypt(path, password, password_confirmation)
        Crypto.decrypt(path, password)
    """

    def __open_file(self, path):
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

    def __check_password(self, password, password2):
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
        elif password != password2:
            return "egal_pwd_error"
        else:
            return password

    def __generate_key_from_pwd(self, password):
        """Génère une clef de chiffrement à partir d'un mot de passe.

        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe

        Returns:
            str -- Clé de chiffrement
        """
        password_provided = password
        password = password_provided.encode()  # Convert to type bytes
        salt = b'\xff\xb6\x9cH\xc7\xf4\x1b\x9ea%Z\xa8+\xeek\x94'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(password))  # Can only use kdf once
        return key

    def encrypt(self, path, password, password2):
        """Chiffrement d'un fichier avec un mot de passe.

        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe
        """
        good_password = self.__check_password(password, password2)
        if good_password == 'len_pwd_error':
            return 'len_pwd_error'
        elif good_password == 'egal_pwd_error':
            return 'egal_pwd_error'
        else:
            key = self.__generate_key_from_pwd(password)

            fn = self.__open_file(path)
            encrypt_file = os.path.join(fn['dirname'], fn['basename'] + '.ch3')

            input_file = path
            output_file = encrypt_file

            with open(input_file, 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)

            return "encrypted file ✅"

    def decrypt(self, path, password):
        """Déchiffrement du fichier avec un mot de passe.

        Arguments:
            password {str} -- Mot de passe
            password2 {str} -- Confirmation du mot de passe
        """
        fn = self.__open_file(path)
        encrypt_file = os.path.join(fn['dirname'], fn['basename'] + '.ch3')

        input_file = path
        output_file = os.path.join(fn['dirname'], fn['basename'][:-4])

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(password)
        encrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

        return "decrypted file ✅"


if __name__ == "__main__":
    crypto = Crypto()
    print('*' * 80)
    print('* CHIFFR3MENT - Encrypt files before sending them to friends or coworkers.     *')
    print('*' * 80)

    pwd = input('Enter password: ')
    pwd2 = input('Enter password confirmation: ')
    path = '/Users/vincent/Documents/code/chiffr3ment/requirements.txt.ch3'

    result = crypto.decrypt(path, pwd, pwd2)
    print(result + '\n')
