from application import create_app
from application.database import DataBase
from flask_socketio import SocketIO
from website import config

# set up
app = create_app()
# for communications between user and server
socketio = SocketIO(app)

@socketio.on('event')
def handle_my_custom_event(json, method=['GET','POST']):
    """
    save messages when receiving it and send it to other clients
    :param json: json
    :param method: GET POST
    :return: None
    """
    data = dict(json)
    if "name" in data:
        db=DataBase()
        db.save_message(data["name"],data["message"])
    socketio.emit("message response", json)

if __name__ == '__main__':
    socketio.run(app, debug=True, host=str(config.Config.SERVER))
