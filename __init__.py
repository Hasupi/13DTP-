from flask import Flask
from flask_login import LoginManager
from prisma import Prisma, register

app = Flask(__name__)
db = Prisma()
db.connect()
register(db)

login_manager = LoginManager()

login_manager.init_app(app)