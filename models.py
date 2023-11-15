from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from init import db, bcrypt 



class User(db.Model):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    email:  Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)

    @classmethod
    def registration(cls, username, pwd, email, first_name, last_name):
        hashed_pwd = bcrypt.generate_password_hash(pwd)
        utf8_hashed_pwd = hashed_pwd.decode("utf8")

        return cls(username=username, password=utf8_hashed_pwd, email=email, first_name=first_name, last_name=last_name)
    

    @classmethod
    def authenticate(cls, username, pwd):
        user = db.get_or_404(User, username)
        
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        
        return False

