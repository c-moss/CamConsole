from flask import render_template
from app.consoleflask import ConsoleFlask
from datetime import datetime

app = ConsoleFlask(__name__)
from app import views
