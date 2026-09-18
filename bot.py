from flask import Flask
import threading, os
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Alive"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
