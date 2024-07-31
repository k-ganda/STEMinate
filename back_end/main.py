from back_end import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)  # Access SocketIO instance from create_app

if __name__ == '__main__':
    socketio.run(app, debug=True)
