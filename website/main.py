import os

from application import create_app
from application.database import DataBase
from flask_socketio import SocketIO
from website import config

# Create Flask app
app = create_app()

# Enable SocketIO with eventlet (install via pip install eventlet)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


# --- SocketIO events ---
@socketio.on('event')
def handle_my_custom_event(json):
    """
    Handles incoming messages from clients
    """
    data = dict(json)
    print("Received:", data)
    if "name" in data and "message" in data:
        try:
            db = DataBase()  # adjust for PostgreSQL if used
            db.save_message(data["name"], data["message"])
            db.close()
        except Exception as e:
            print("DB error:", e)
    socketio.emit("message response", json)  # broadcast to all clients


# --- Run app ---
if __name__ == "__main__":
    # Use the PORT environment variable assigned by Azure, default 5000 for local testing
    port = int(os.environ.get("PORT", 5000))

    # Important: host 0.0.0.0 so Azure can route traffic
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=True,
        use_reloader=False  # prevents multiple processes on Azure
    )
    # socketio.run(app, debug=True, host=str(config.Config.SERVER))
    # socketio.run(app, host=config.Config.SERVER, port=config.Config.PORT, debug=config.Config.FLASK_DEBUG)
