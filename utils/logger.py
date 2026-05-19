import requests
import threading
import uuid
import json

class SupabaseLogger:
    def __init__(self, user_id):
        self.user_id = user_id
        self.supabase_url = "https://sgofneigxhkgbvzujkrw.supabase.co/rest/v1/app_logs"
        self.anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNnb2ZuZWlneGhrZ2J2enVqa3J3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg4MzEwMjEsImV4cCI6MjA5NDQwNzAyMX0.CDGLBT29Z3A9xKBgo8ELdwFXT_fnNYKnvZa7kh1azS8"

    def enviar_log(self, event_type):

        def _hilo_envio():
            headers = {
                "apikey": self.anon_key,
                "Authorization": f"Bearer {self.anon_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            
            data = {
                "event_type": event_type,
                "user_id": self.user_id
            }
            
            try:
                requests.post(self.supabase_url, headers=headers, json=data, timeout=3)
            except Exception as e:
                print(f"Error al enviar el log ({event_type}): {e}")
                pass

        threading.Thread(target=_hilo_envio, daemon=True).start()