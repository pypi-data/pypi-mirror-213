from .settings import Settings
import pyrebase


class Session(object):

    def __init__(self, email, password) -> None:
        firebase = pyrebase.initialize_app(Settings.setup)
        self.auth = firebase.auth()
        self.login = self.auth.sign_in_with_email_and_password(email, password)
        self.db = firebase.database()

    def create_user(self):

        email = input("ingresa email: ")
        password = input("ingresa contraseña: ")
        self.auth.create_user_with_email_and_password(email, password)

    def define_admin(self):

        uid = input("ingresa uid: ")
        self.db.child("admin").update({uid: uid}, self.login['idToken'])
