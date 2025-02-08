# SRT Sentinel

A tool to monitor SRT feeds and switch OBS scenes based on feed health.

## Features

- Monitors SRT feed stats (bitrate, packet loss, etc.).
- Switches OBS scenes if the feed becomes unhealthy.
- Configurable via `.env` file.
- Lightweight and easy to use.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/srt-sentinel.git
   cd srt-sentinel
   ```

1. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

1. **Configure the .env file**:

   ```bash
   cp .env.example .env
   code .env  # Or open with your favorite text editor
   ```

## Usage

Run the script:

```bash
python srt_sentinel.py
```

The script will:

- Check the OBS WebSocket connection.
- Verify the SRT stats page is accessible.
- Start monitoring the SRT feed and switch OBS scenes as needed.

## Configuration

All configuration options are documented in .env.example. Copy this file to .env and fill in your settings.

## License

This project is licensed under the **GNU AGPL-3.0**.
If you use this software in a **commercial setting** (e.g., as part of a paid service or product), you are required to either:

1. Open-source any modifications and comply with AGPL-3.0.
2. Obtain a **commercial license**, see COMMERCIAL_LICENSE.

For commercial support, contact us at [YOUR EMAIL].
