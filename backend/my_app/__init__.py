from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

import sys, os
## 상위 폴더 경로 append
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

socketio = SocketIO()
app = Flask(__name__, template_folder='front')

def create_app():

    with app.app_context():
        CORS(app, origins=["http://localhost:3000"])

        from my_app.router.main_router import bp_main
        app.register_blueprint(bp_main)

        print('socketio start')
        socketio.init_app(app, cors_allowed_origins="http://localhost:3000")
        # socketio.init_app(app)

        return app
