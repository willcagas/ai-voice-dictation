# main.py
"""
Main entry point for the AI Voice Dictation application.

Orchestrates all components:
- HotkeyListener: Detects PTT key down/up
- AudioRecorder: Records audio while PTT is held
- Transcriber: Converts audio to text via whisper.cpp
- Formatter: Rewrites transcript via cloud LLM
- Injector: Copies to clipboard and optionally pastes
"""

import signal
import sys
from typing import Optional

from .audio import AudioRecorder
from .config import Config
from .format_llm import Formatter
from .hotkeys import HotkeyListener
from .inject import Injector
from .transcribe import Transcriber
from .utils import get_temp_audio_path, setup_logging

logger = setup_logging()


class DictationApp:
    """Main application orchestrating all dictation components."""
    
    def __init__(self):
        """Initialize all components."""
        logger.info("Initializing AI Voice Dictation...")
        
        self.config = Config()
        self.audio = AudioRecorder()
        self.transcriber = Transcriber(self.config)
        self.formatter = Formatter(self.config)
        self.injector = Injector()
        
        self.hotkey_listener: Optional[HotkeyListener] = None
        self._running = False
    
    def on_ptt_press(self) -> None:
        """Handle PTT key press - start recording."""
        logger.info("🎤 Recording...")
        self.audio.start_recording()
    
    def on_ptt_release(self) -> None:
        """Handle PTT key release - process audio pipeline."""
        temp_path = get_temp_audio_path()
        
        # Stop recording and save audio
        if not self.audio.stop_recording(temp_path):
            logger.warning("No audio recorded")
            return
        
        # Transcribe audio
        logger.info("📝 Transcribing...")
        raw_text = self.transcriber.transcribe(temp_path)
        
        if not raw_text:
            logger.warning("No transcript produced")
            return
        
        logger.info(f"Raw: {raw_text[:100]}...")
        
        # Format with LLM
        logger.info(f"✨ Formatting ({self.config.mode} mode)...")
        formatted_text = self.formatter.format(raw_text, self.config.mode)
        
        logger.info(f"Formatted: {formatted_text[:100]}...")
        
        # Inject to clipboard (and optionally paste)
        logger.info("📋 Copying to clipboard...")
        self.injector.inject(formatted_text, self.config.auto_paste)
        
        logger.info("✅ Done!")
    
    def run(self) -> None:
        """Start the application main loop."""
        self._running = True
        
        # Set up hotkey listener
        self.hotkey_listener = HotkeyListener(
            ptt_key=self.config.ptt_key,
            on_press=self.on_ptt_press,
            on_release=self.on_ptt_release
        )
        
        # Handle Ctrl+C gracefully
        def signal_handler(signum, frame):
            logger.info("\nShutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start listening
        self.hotkey_listener.start()
        
        logger.info("=" * 50)
        logger.info("AI Voice Dictation is running!")
        logger.info(f"Mode: {self.config.mode}")
        logger.info(f"PTT Key: {self.config.ptt_key}")
        logger.info(f"Auto-paste: {self.config.auto_paste}")
        logger.info("=" * 50)
        logger.info("Hold PTT key to record, release to process.")
        logger.info("Press Ctrl+C to quit.")
        
        # Block until stopped
        self.hotkey_listener.wait()
    
    def stop(self) -> None:
        """Stop the application."""
        self._running = False
        if self.hotkey_listener:
            self.hotkey_listener.stop()


def main():
    """Main entry point."""
    app = DictationApp()
    app.run()


if __name__ == "__main__":
    main()
