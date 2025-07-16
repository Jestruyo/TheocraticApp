import time
from threading import Thread
from app.extensions import twilio_client
from ..utils import TWILIO_PHONE
from ..state import user_state

def check_inactive_sessions():
    while True:
        now = time.time()
        for number, data in list(user_state.items()):
            last = data.get('last_activity', 0)
            if (now - last) > 180 and not data.get('inactivity_notified', False):
                try:
                    twilio_client.messages.create(
                        body='⏳ He notado que no has interactuado hasta luego 👋...',
                        from_=TWILIO_PHONE,
                        to=number
                    )
                    user_state[number]['inactivity_notified'] = True
                except Exception as e:
                    print(f"Error enviando mensaje a {number}: {e}")
        time.sleep(30)

def start_monitor_thread():
    thread = Thread(target=check_inactive_sessions, daemon=True)
    thread.start()
