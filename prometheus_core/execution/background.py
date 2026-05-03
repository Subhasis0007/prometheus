import time
import threading

def background_metacognition():
    while True:
        print("[Metacognition] Background thinking... (improving skills)")
        time.sleep(300)  # Every 5 minutes

def start_background():
    thread = threading.Thread(target=background_metacognition, daemon=True)
    thread.start()
    print("[Metacognition] Background process started")
