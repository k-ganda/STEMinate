from app import create_app
from flask_socketio import SocketIO


if __name__ == '__main__':
    app = create_app()
    socketio = SocketIO(app)  # Access SocketIO instance from create_app
    socketio.run(app, debug=True)
    