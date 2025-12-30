import google.generativeai as genai
from openai import OpenAI
from ..config.settings import settings
from typing import List, Dict, Any, Optional
import asyncio
import logging


class LLMService:
    def __init__(self):
        self.gemini_service = None
        self.openrouter_service = None
        self.primary_service = None

        # Initialize services based on available API keys
        if settings.openrouter_api_key:
            try:
                self.openrouter_service = OpenRouterService()
                self.primary_service = self.openrouter_service
                logging.info("Using OpenRouter as primary LLM service")
            except Exception as e:
                logging.error(f"Failed to initialize OpenRouter service: {e}")

        if settings.gemini_api_key and settings.gemini_api_key != "AIzaSyAjDfTQv98Bk8aLWBgvKH2lWAsdlfNPE24":  # Default placeholder
            try:
                self.gemini_service = GeminiService()
                if self.primary_service is None:
                    self.primary_service = self.gemini_service
                    logging.info("Using Gemini as primary LLM service")
            except Exception as e:
                logging.error(f"Failed to initialize Gemini service: {e}")

        if self.primary_service is None:
            logging.warning("No LLM service initialized - will use fallback local responses")

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate response using the primary available service
        """
        if self.primary_service:
            try:
                return await self.primary_service.generate_response(prompt, context)
            except Exception as e:
                logging.error(f"Primary service failed: {e}")
                # Fallback to other service if available
                if self.primary_service == self.openrouter_service and self.gemini_service:
                    return await self.gemini_service.generate_response(prompt, context)
                elif self.primary_service == self.gemini_service and self.openrouter_service:
                    return await self.openrouter_service.generate_response(prompt, context)

        # Ultimate fallback
        return "Sorry, the AI service is not available at the moment."

    def generate_streaming_response(self, prompt: str, context: Optional[str] = None):
        """
        Generate streaming response using the primary available service
        """
        if self.primary_service:
            try:
                return self.primary_service.generate_streaming_response(prompt, context)
            except Exception as e:
                logging.error(f"Primary service streaming failed: {e}")
                # Fallback to other service if available
                if self.primary_service == self.openrouter_service and self.gemini_service:
                    return self.gemini_service.generate_streaming_response(prompt, context)
                elif self.primary_service == self.gemini_service and self.openrouter_service:
                    return self.openrouter_service.generate_streaming_response(prompt, context)

        # Ultimate fallback
        yield "Sorry, the AI service is not available at the moment."

    async def check_connection(self) -> bool:
        """
        Check if any LLM service is available
        """
        return self.primary_service is not None and await self.primary_service.check_connection()


class OpenRouterService:
    def __init__(self):
        try:
            # Configure OpenAI client for OpenRouter
            self.client = OpenAI(
                api_key=settings.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = settings.openrouter_model or "openai/gpt-3.5-turbo"  # Default model - using a valid OpenRouter model
            self.is_connected = self.check_connection_sync()
        except Exception as e:
            logging.error(f"Failed to initialize OpenRouter client: {e}")
            self.client = None
            self.is_connected = False

    def check_connection_sync(self) -> bool:
        """
        Synchronous check if OpenRouter connection is available
        """
        try:
            return bool(self.client and settings.openrouter_api_key)
        except Exception as e:
            logging.error(f"OpenRouter connection failed: {e}")
            return False

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate response using OpenRouter model
        """
        if not self.client:
            logging.error("OpenRouter client not initialized")
            return "Sorry, the AI service is not available."

        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Create the messages array for the OpenRouter API
            messages = [
                {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. ONLY answer questions based on the provided context from the textbook. If a question is not related to humanoid robotics, physical AI, or the book content, respond with: 'I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content.' Be helpful but stay within the scope of the textbook."},
                {"role": "user", "content": full_prompt}
            ]

            # Make the async call to OpenRouter
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
            )

            return response.choices[0].message.content if response.choices[0].message.content else "I couldn't generate a response."
        except Exception as e:
            logging.error(f"Error generating response with OpenRouter: {e}")
            return "Sorry, I encountered an error processing your request."

    def generate_streaming_response(self, prompt: str, context: Optional[str] = None):
        """
        Generate streaming response using OpenRouter model
        """
        if not self.client:
            logging.error("OpenRouter client not initialized")
            yield "Sorry, the AI service is not available."
            return

        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Create the messages array for the OpenRouter API
            messages = [
                {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. ONLY answer questions based on the provided context from the textbook. If a question is not related to humanoid robotics, physical AI, or the book content, respond with: 'I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content.' Be helpful but stay within the scope of the textbook."},
                {"role": "user", "content": full_prompt}
            ]

            # Create streaming completion
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logging.error(f"Error generating streaming response with OpenRouter: {e}")
            yield "Sorry, I encountered an error processing your request."

    async def check_connection(self) -> bool:
        """
        Check if OpenRouter connection is available (async wrapper)
        """
        return self.is_connected


class GeminiService:
    def __init__(self):
        try:
            genai.configure(api_key=settings.gemini_api_key)
            # Using gemini-2.0-flash instead of gemini-pro which might not be available
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
            # Just check if model exists, actual validation would require a call
            return bool(self.model)
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