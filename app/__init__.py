from .extensions import app
from .routes.enviar import enviar_bp
from .routes.webhook import webhook_bp
from .services.inactivity import start_monitor_thread
import atexit

def cleanup():
    print("Cerrando hilos de monitoreo...")

def create_app():
    app.register_blueprint(enviar_bp)
    app.register_blueprint(webhook_bp)
    start_monitor_thread()
    atexit.register(cleanup)
    return app
