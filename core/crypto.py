import base64
import os

# pip install cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypto:
    """Encryption decryption of files.

    Use:
     - Crypto.encrypt(path, password, password_confirmation)
     - Crypto.decrypt(path, password)
    """

    def __open_file(self, path):
        """Retrieves the path of the file to open and returns the path, file 
        name, and file type.

        Arguments:
         - path {str} -- Path to the file.

        Returns:
         - dict -- dirname, basename, extension
        """
        dirname, basename = os.path.split(path)
        extension = os.path.splitext(basename)[1]
        basename = os.path.splitext(path)[0]

        return {'dirname': dirname, 'basename': basename, 'extension': extension}

    def __check_password(self, password, password2):
        """Checks the length of the password (greater than 6 characters) and 
        checks if the password is identical to the verification.

        Arguments:
         - password {str} -- Password
         - password2 {str} -- Password confirmation

        Returns:
         - str -- Error messages or "pwd_ok"
        """
        if len(password) < 6:
            return "len_pwd_error"
        elif password != password2:
            return "egal_pwd_error"
        else:
            return password

    def __generate_key_from_pwd(self, password):
        """Generates an encryption key from a password.

        Arguments:
         - password {str} -- Password
         - password2 {str} -- Password confirmation

        Returns:
         - str -- Encryption key
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
        """Encrypting a file with a password.

        Arguments:
         - path {str} -- Path to the file to encrypt
         - password {str} -- Password
         - password2 {str} -- Password confirmation

        Returns:
         - str -- Error or confirmation messages
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
            extension = fernet.encrypt(bytes(fn['extension'], encoding='utf8'))

            with open(output_file, 'wb') as f:
                f.write(encrypted + b'#' + extension)

            return "encrypted file"

    def decrypt(self, path, password):
        """Decrypting the file with a password.

        Arguments:
         - path {str} -- Path to the file to encrypt
         - password {str} -- Password

        Returns:
         - str -- Error or confirmation messages
        """
        key = self.__generate_key_from_pwd(password)
        fn = self.__open_file(path)

        input_file = path

        with open(input_file, 'rb') as f:
            data = f.read()
            content, extension = data.split(b'#')

        try:
            fernet = Fernet(key)
            ext = fernet.decrypt(extension)
            encrypted = fernet.decrypt(content)

            output_file = os.path.join(
                fn['dirname'], fn['basename'] + ext.decode())

            with open(output_file, 'wb') as f:
                f.write(encrypted)
        except:
            return "incorrect_pwd"

        return "decrypted file"


if __name__ == "__main__":
    from getpass import getpass
    from tkinter import filedialog
    from tkinter import Tk

    crypto = Crypto()
    os.system('clear')
    print('*' * 80)
    print('* CHIFFR3MENT - Encrypt the files before sending them to friends or colleagues *')
    print('*' * 80)

    Tk().withdraw()
    path = filedialog.askopenfilename(title="Open file")

    if os.path.splitext(path)[1] == '.ch3':
        print('-- File encrypted --')
        pwd = getpass('Enter password: ')
        result = crypto.decrypt(path, pwd)
        print('==> ' + result + '\n')

    else:
        print('-- File not encrypted --')
        pwd = getpass('Enter password: ')
        pwd2 = getpass('Enter password confirmation: ')
        result = crypto.encrypt(path, pwd, pwd2)
        print('==> ' + result + '\n')
