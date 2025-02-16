# **SRT Sentinel** 🚨🎥

A **lightweight** yet **powerful** tool to monitor **Secure Reliable Transport (SRT)** feeds and **automatically switch OBS scenes** based on stream health.

Never get caught with a frozen feed again—SRT Sentinel **watches your stream like a hawk** and ensures your viewers see only the best!

Note: I made chatgpt generate this README

---

## 🚀 **Features**

- 📡 **Live SRT Monitoring** – Tracks bitrate, packet loss, and stream availability.
- 🔄 **Auto Scene Switching** – Seamlessly transitions between primary and backup OBS scenes.
- ⚙️ **Fully Configurable** – Uses a simple `.env` file for setup.
- ⚡ **Fast & Lightweight** – Runs efficiently in the background without bloating your system.
- 📜 **Open-Source & Extensible** – Modify it to fit your workflow.

---

## 🛠 **Installation**

### 1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-username/srt-sentinel.git
cd srt-sentinel
```

### 2️⃣ **Install dependencies**

Ensure [Poetry](https://python-poetry.org/docs/) is installed, then run:

```bash
poetry install
```

### 3️⃣ **Configure the `.env` file**

```bash
cp .env.example .env
code .env  # Open with your preferred editor
```

Fill in the necessary settings (OBS WebSocket, SRT server URL, bitrate thresholds, etc.).

---

## 🎯 **Usage**

Run the tool with:

```bash
poetry run srt-sentinel
```

### What Happens? 🤖

✔️ Checks connection to **OBS WebSocket**.

✔️ Fetches stream stats from the **SRT server**.

✔️ **Monitors feed health** and detects low bitrate or stream failures.

✔️ **Switches scenes automatically** if needed.

Your stream stays **smooth** even when things go wrong!

---

## ⚙️ **Configuration**

All settings are defined in the `.env` file.

Check `.env.example` for available options like:

- **OBS WebSocket connection details** (host, port, password).
- **SRT monitoring settings** (stats URL, bitrate threshold, publishers).
- **Scene names** (main scene & backup scene for failover).
- **Polling interval** (how often it checks stream health).

💡 _Customize it to fit your workflow!_

---

## ✅ **TODO & Contribution Ideas**

Want to contribute? Here are some great places to start:

### 🧪 **1. Add Tests (Pytest)**

- The project currently **lacks automated tests**—adding **unit tests** for key components (e.g., `OBSClient`, `SRTClient`, `SRTSentinel`) would make development safer.
- Consider using **pytest + unittest.mock** for mocking network calls.
- Add **integration tests** to simulate switching between scenes based on test SRT data.

### 🔧 **2. Make Clients Modular & Extendable**

- Right now, **OBS and SLS monitoring are hardcoded**.
- Refactor `OBSClient` and `SLSClient` into **modular clients** that can be dynamically loaded via config.
- Add support for **other protocols** (e.g., RTMP monitoring, WebRTC, or alternative scene switchers).
- Allow multiple **"actions"** when a stream fails (e.g., triggering a webhook, running a script, sending a Discord alert).

### 📈 **3. Improve Logging & Debugging**

- Add **debug-level logging** to track OBS commands & responses.
- Allow enabling verbose mode via `.env` (e.g., `LOG_LEVEL=DEBUG`).
- Write logs to a **rotating log file** for better debugging.

### 🌍 **4. Web Dashboard for Monitoring**

- Build a **minimal web interface** to display real-time feed health.
- Use **FastAPI + WebSockets** to push live updates to a frontend (Vue/React).
- Would allow remote monitoring without needing OBS logs.

### 📦 **5. Package It for Easier Installation**

- Create a **Docker container** so users can run it without setting up Python.
- Publish a **PyPI package** (`pip install srt-sentinel`).

💡 Got ideas? Open an issue or send a pull request!

---

## 📝 **License**

SRT Sentinel is licensed under **GNU AGPL-3.0**.

If you plan to use it in a **commercial setting** (e.g., part of a paid service or product), you must:

1. Open-source your modifications under AGPL-3.0 **or**
2. Obtain a **commercial license** (see `COMMERCIAL_LICENSE`).

📬 For licensing inquiries, contact us at **[http://scr.im/22q7](http://scr.im/22q7)**.

---

## 🎤 **Contributions & Feedback**

🚀 Have ideas? Found a bug? Want to improve it?

- Open an **issue** or **pull request** on GitHub.
- Let’s build something awesome together! 🛠
