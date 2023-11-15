from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app import db, app, bcrypt 


with app.app_context():
    db.drop_all()
    db.create_all()


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
    def registration(cls, username, pwd):
        hashed_pwd = bcrypt.generate_password_hash(pwd)
        utf8_hashed_pwd = hashed_pwd.decode("utf8")

        return cls(username=username, password=utf8_hashed_pwd)
    

    @classmethod
    def authenticate(cls, username, pwd):
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
        
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        
        return False

