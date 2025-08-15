# 🔑 Simple Remote Keylogger

> **Disclaimer**  
> This project is for **educational and ethical purposes only**.  
> Use it **only** on systems you own or have explicit permission to monitor.  
> Unauthorized use is **illegal** and punishable by law.

---

## 📌 Overview
This project is a **client-server based remote keylogger** built with Python.  
It records keystrokes on a client machine, logs the program where the keystrokes were typed, and sends the data to a remote server in real-time.

It’s designed for **cybersecurity research, ethical hacking training, and digital forensics**.

---

## ⚙️ Features
✅ Captures keystrokes in real-time  
✅ Detects **which program/window** was active when the key was pressed  
✅ Sends logs to a **remote Flask server**  
✅ Stores logs on the server side  
✅ Easy to deploy & customize  
✅ Works over LAN or Internet (via ngrok / VPS hosting)  

---

## 📂 Project Structure
📦 Python-Keylogger

┣ 📜 client.py # Keylogger client (runs on target system)

┣ 📜 server.py # Flask server to receive and store logs

┣ 📜 requirements.txt # Python dependencies

┗ 📜 README.md # Project documentation

---


---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ImLegendAdi/PRODIGY_CS_04.git
cd <repo>
python3 server.py
python3 client.py
```


