from flask import Flask
from .views.tool import tool
app = Flask(__name__)
app.register_blueprint(tool)
