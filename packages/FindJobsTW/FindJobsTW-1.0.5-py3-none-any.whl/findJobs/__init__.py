from flask import Flask
from .app import app

def create_app():
    # app 是從 app.py 中匯入的 Flask 應用
    return app