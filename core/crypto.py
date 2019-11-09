import os

class Crypto:

    def open_file(self, path):
        dirname, basename = os.path.split(path)

        extension = os.path.splitext(basename)[1]

        print(f'{dirname}, {basename}, {extension}')
        

    def check_password(self, password, password2):
        if len(password) > 5:
            if password != password2:
                return False
            else:
                return True
        else:
            print('moins de 6')
            return False


if __name__ == "__main__":
    crypto = Crypto()
    # path = input("Dir filename: ")
    # crypto.open_file(path)

    print(crypto.check_password('pass', 'password'))