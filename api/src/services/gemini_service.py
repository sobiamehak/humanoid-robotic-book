import google.generativeai as genai
from src.config.settings import settings
from typing import List, Dict, Any, Optional
import asyncio
import logging


class GeminiService:
    def __init__(self):
        try:
            genai.configure(api_key=settings.gemini_api_key)
            # Using gemini-1.5-flash instead of gemini-pro which might not be available
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.is_connected = self.check_connection_sync()
        except Exception as e:
            logging.error(f"Failed to initialize Gemini client: {e}")
            self.model = None
            self.is_connected = False

    def check_connection_sync(self) -> bool:
        """
        Synchronous check if Gemini connection is available
        """
        try:
            # Try to validate the API key by making a simple call
            if self.model:
                # Just check if model exists, actual validation would require a call
                return True
        except Exception as e:
            logging.error(f"Gemini connection failed: {e}")
            return False

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate response using Gemini model
        """
        if not self.model:
            logging.error("Gemini model not initialized")
            return "Sorry, the AI service is not available."

        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Run the synchronous operation in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: self.model.generate_content(full_prompt))
            return response.text if response.text else "I couldn't generate a response."
        except Exception as e:
            logging.error(f"Error generating response with Gemini: {e}")
            return "Sorry, I encountered an error processing your request."

    def generate_streaming_response(self, prompt: str, context: Optional[str] = None):
        """
        Generate streaming response using Gemini model
        """
        if not self.model:
            logging.error("Gemini model not initialized")
            yield "Sorry, the AI service is not available."
            return

        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Use the synchronous streaming method
            response = self.model.generate_content(full_prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logging.error(f"Error generating streaming response with Gemini: {e}")
            yield "Sorry, I encountered an error processing your request."

    async def check_connection(self) -> bool:
        """
        Check if Gemini connection is available (async wrapper)
        """
        return self.is_connected