from extension import db
from extension import bcrypt
from tool import Md5


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(60), unique=True,
                         nullable=False, index=True)
    password = db.Column(db.String(400), unique=True, nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=True, index=True)
    github = db.Column(db.String(400), unique=True, nullable=True)
    bilibili = db.Column(db.String(400), unique=True, nullable=True)
    showName = db.Column(db.String(60), unique=True,
                         nullable=True, default=username)
    mail_hash = db.Column(db.String(100), unique=True,
                          nullable=True)

    def __init__(self, *args, **kwargs):
        mail = kwargs.get('mail')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.mail_hash = Md5(mail)
        self.mail = mail
        self.username = username
        self .password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        print(password)
        return bcrypt.check_password_hash(self.password, password)

    def save_on(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False
