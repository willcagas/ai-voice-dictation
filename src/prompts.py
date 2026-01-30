# prompts.py
"""
LLM prompt templates for dictation formatting.

Contains system prompts and mode-specific instructions for the formatter.
"""

from typing import Literal

# System prompt - shared constraints for all modes
SYSTEM_PROMPT = """You are a dictation formatter. Your job is to rewrite speech-to-text transcripts into polished text.

Rules:
1. Rewrite without adding any new information
2. Preserve all names, dates, numbers, and URLs exactly as spoken
3. If something is unclear, keep the original wording
4. Return ONLY the rewritten text - no markdown formatting, no quotes, no explanations
5. Never invent or assume details that weren't in the original"""

# Mode-specific prompts
EMAIL_MODE_PROMPT = """Rewrite this transcript as a professional email:
- Use complete, well-structured sentences
- Apply proper punctuation and paragraphing
- Keep it concise but polished
- Only include greeting/signoff if the speaker said one

Transcript: {transcript}"""

MESSAGE_MODE_PROMPT = """Rewrite this transcript as a casual message:
- Keep it short and conversational
- Minimal punctuation is fine
- No formal greetings or signoffs
- Match the speaker's casual tone

Transcript: {transcript}"""


def get_user_prompt(mode: Literal["email", "message"], transcript: str) -> str:
    """
    Build the user prompt for the given mode and transcript.
    
    Args:
        mode: Either "email" or "message"
        transcript: Raw speech-to-text transcript
    
    Returns:
        Formatted user prompt string
    """
    if mode == "email":
        return EMAIL_MODE_PROMPT.format(transcript=transcript)
    else:
        return MESSAGE_MODE_PROMPT.format(transcript=transcript)
