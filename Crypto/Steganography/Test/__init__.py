from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c03bcfa7c0f29d2192ac0b84991c693f'
bcrypt = Bcrypt(app)

from Test import routes
