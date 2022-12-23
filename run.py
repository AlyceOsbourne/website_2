from flask import Flask
from modules import setup_app

if __name__ == '__main__':
    app = Flask(__name__)
    setup_app(app).run(
            debug = True,
            host = '0.0.0.0',
            port = 5000,
    )
