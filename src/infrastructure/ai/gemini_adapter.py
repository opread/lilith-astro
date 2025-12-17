"""Gemini AI adapter for text generation."""

import google.generativeai as genai


class GeminiAdapter:
    """Adapter for Google Gemini AI text generation."""

    def __init__(self, api_key: str):
        """Initialize the Gemini adapter.

        Args:
            api_key: Google AI API key.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_text(self, prompt: str) -> str:
        """Generate text using the Gemini model.

        Args:
            prompt: The prompt to send to the model.

        Returns:
            The generated text.
        """
        response = self.model.generate_content(prompt)
        return response.text