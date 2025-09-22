from application import create_app
from application.database import DataBase
from flask_socketio import SocketIO
from website import config

# set up
app = create_app()
app.secret_key = "8903"
# for communications between user and server
socketio = SocketIO(app)

@socketio.on('event')
def handle_my_custom_event(json):
    """
    communication function for event
    save messages after received data from web server, send data to other clients
    :param json: json
    :return: None
    """
    data = dict(json)
    if "name" in data:
        db=DataBase()
        db.save_message(data["name"],data["message"])
    socketio.emit("message response", json)

# run the app
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    # socketio.run(app, debug=True, host=str(config.Config.SERVER))
    # socketio.run(app, host=config.Config.SERVER, port=config.Config.PORT, debug=config.Config.FLASK_DEBUG)
