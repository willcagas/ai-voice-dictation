
<div align="center">
  <img src="assets/avid_logo.png" width="128" height="128" alt="AViD Logo">
  <h1>AViD</h1>
  <h3>AI VoIce Dictation</h3>
  <p>Experimental internal tool for high-speed, AI-formatted voice input on macOS.</p>
</div>

---

> **internal-tool**: This project is built primarily for the creator's personal workflow. <br>
> You are free to fork and use it, but you must bring your own **OpenAI API Key** for the AI formatting features.

## Overview

**AViD** allows you to dictate text using Push-to-Talk, transcribing it locally with `whisper.cpp` for speed and privacy, then instantly rewriting it via GPT-4o into polished text before auto-pasting it into your active window.

- **Local Transcription**: Uses `whisper.cpp` (Metal accelerated) for fast, private ASR.
- **AI Formatting**: Cloud LLM rewrites your raw speech into structured text.
- **Push-to-Talk**: Hold `Right Option` (configurable) to record. Release to process.
- **4 Output Modes**:
  - **Message**: Casual, conversational (default)
  - **Email**: Professional, complete sentences
  - **Notes**: Semi-structured, scannable notes
  - **Prompt**: AI prompt engineering using CO-STAR framework
- **Auto-Paste**: Directly injects the formatted text into your focused application.

## Prerequisites

- **macOS** (Optimized for Apple Silicon)
- **Python 3.11+**
- **Homebrew**
- **OpenAI API Key** (Required for LLM formatting)

## Setup Guide

### 1. Install System Dependencies

```bash
brew install whisper-cpp
```

### 2. Download Whisper Model

Download a model for local transcription (Base English recommended for speed/accuracy balance):

```bash
mkdir -p ~/models/whisper
cd ~/models/whisper
curl -L -o ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

### 3. Clone & Python Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/avid.git
cd avid

# Setup Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python Requirements
pip install sounddevice numpy pynput python-dotenv requests scipy pywebview
```

### 4. Configuration

Create your `.env` file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API Key:
```
OPENAI_API_KEY=sk-your-key-here
PTT_KEY=alt_r
AUTO_PASTE=true
```

## Permissions

AViD needs system permissions to function correctly:
1.  **Microphone**: For recording audio.
2.  **Accessibility**: For simulating keystrokes (Auto-Paste). Go to **System Settings > Privacy & Security > Accessibility** and add your **Terminal** or IDE (e.g., VSCode, iTerm).

## Usage

### Manual Run

To test the application with the UI overlay:

```bash
source .venv/bin/activate
python -m src.main --ui
```

- **Hold** `Right Option` to record.
- **Speak** your thought.
- **Release** to process.
- The overlay will show the status; text will auto-paste when ready.

### Install as Background Service (Recommended)

To have AViD run automatically at login (and restart if it crashes):

```bash
./scripts/install_launchagent.sh
```

> **Note**: If you encounter a "Permission denied" error or "Operation not permitted", run this command to fix ownership of your LaunchAgents directory:
> ```bash
> sudo chown -R $(whoami) ~/Library/LaunchAgents
> // And try installing again
> ./scripts/install_launchagent.sh
> ```

### Making Changes

If you modify the code, you can instantly reload the background service without restarting your computer:

```bash
./scripts/reload.sh
```

## Project Structure

- `src/main.py`: Application entry point.
- `src/audio.py`: Audio recording via `sounddevice`.
- `src/transcribe.py`: Local transcription handling.
- `src/format_llm.py`: Logic for GPT-4o formatting.
- `src/ui/`: WebView based UI overlay (HTML/CSS/JS).
- `launchd/`: macOS LaunchAgent configuration.

## License

MIT
