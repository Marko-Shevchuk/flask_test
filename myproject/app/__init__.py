from flask import Flask

app = Flask(__name__)
app.secret_key = "pleasedosha512fiwkeokweowoefkm3r8j"

from app import views
