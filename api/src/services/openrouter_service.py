# import openai
# from src.config.settings import settings
# from typing import List, Dict, Any, Optional
# import asyncio
# import logging

# import json
# class OpenRouterService:
#     def __init__(self):
#         try:
#             # Configure OpenAI to use OpenRouter
#             openai.api_key = settings.openrouter_api_key
#             openai.base_url = "https://openrouter.ai/api/v1"
#             self.model = settings.openrouter_model or "google/gemini-pro"  # Default model
#             self.is_connected = self.check_connection_sync()
#         except Exception as e:
#             logging.error(f"Failed to initialize OpenRouter client: {e}")
#             self.is_connected = False

#     def check_connection_sync(self) -> bool:
#         """
#         Synchronous check if OpenRouter connection is available
#         """
#         try:
#             # Just check if we have an API key set 
#             return bool(settings.openrouter_api_key)
#         except Exception as e:
#             logging.error(f"OpenRouter connection failed: {e}")
#             return False

#     async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
#         """
#         Generate response using OpenRouter model
#         """
#         if not settings.openrouter_api_key:
#             logging.error("OpenRouter API key not configured")
#             return "Sorry, the AI service is not available."

#         try:
#             full_prompt = prompt
#             if context:
#                 full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

#             # Create the messages array for the OpenRouter API
#             messages = [
#                 {"role": "system", "content": "You are a helpful AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided context to answer questions accurately and helpfully."},
#                 {"role": "user", "content": full_prompt}
#             ]

#             # Make the async call to OpenRouter
#             loop = asyncio.get_event_loop()
#             response = await loop.run_in_executor(
#                 None,
#                 lambda: openai.chat.completions.create(
#                     model=self.model,
#                     messages=messages,
#                     temperature=0.7,
#                     max_tokens=1000
#                 )
#             )

#             return response.choices[0].message.content if response.choices[0].message.content else "I couldn't generate a response."
#         except Exception as e:
#             logging.error(f"Error generating response with OpenRouter: {e}")
#             return "Sorry, I encountered an error processing your request."

#     def generate_streaming_response(self, prompt: str, context: Optional[str] = None):
#         """
#         Generate streaming response using OpenRouter model
#         """
#         if not settings.openrouter_api_key:
#             logging.error("OpenRouter API key not configured")
#             yield "Sorry, the AI service is not available."
#             return

#         try:
#             full_prompt = prompt
#             if context:
#                 full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

#             # Create the messages array for the OpenRouter API
#             messages = [
#                 {"role": "system", "content": "You are a helpful AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided context to answer questions accurately and helpfully."},
#                 {"role": "user", "content": full_prompt}
#             ]

#             # Create streaming completion
#             stream = openai.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=0.7,
#                 max_tokens=1000,
#                 stream=True
#             )

#             for chunk in stream:
#                 if chunk.choices[0].delta.content:
#                     yield {"event": "chunk", "data": chunk.choices[0].delta.content}

#         except Exception as e:
#             logging.error(f"Error generating streaming response with OpenRouter: {e}")
#             yield "Sorry, I encountered an error processing your request."

#     async def check_connection(self) -> bool:
#         """
#         Check if OpenRouter connection is available (async wrapper)
#         """
#         return self.is_connected



import openai
from src.config.settings import settings
from typing import Optional
import asyncio
import logging
import json  # ✅ Required for JSON SSE formatting

class OpenRouterService:
    def __init__(self):
        try:
            # Configure OpenAI to use OpenRouter
            openai.api_key = settings.openrouter_api_key
            openai.base_url = "https://openrouter.ai/api/v1"
            self.model = settings.openrouter_model or "google/gemini-pro"  # Default model
            self.is_connected = self.check_connection_sync()
        except Exception as e:
            logging.error(f"Failed to initialize OpenRouter client: {e}")
            self.is_connected = False

    def check_connection_sync(self) -> bool:
        """Synchronous check if OpenRouter connection is available"""
        try:
            return bool(settings.openrouter_api_key)
        except Exception as e:
            logging.error(f"OpenRouter connection failed: {e}")
            return False

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response using OpenRouter model (non-streaming)"""
        if not settings.openrouter_api_key:
            logging.error("OpenRouter API key not configured")
            return "Sorry, the AI service is not available."

        try:
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}" if context else prompt

            messages = [
                {"role": "system", "content": "You are a helpful AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided context to answer questions accurately and helpfully."},
                {"role": "user", "content": full_prompt}
            ]

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: openai.chat.completions.create(
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
        """Generate streaming response using OpenRouter model with proper SSE JSON format"""
        if not settings.openrouter_api_key:
            logging.error("OpenRouter API key not configured")
            yield json.dumps({
                "event": "chunk",
                "data": "Sorry, the AI service is not available."
            })
            yield json.dumps({"event": "done"})
            return

        try:
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}" if context else prompt

            messages = [
                {"role": "system", "content": "You are a helpful AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided context to answer questions accurately and helpfully."},
                {"role": "user", "content": full_prompt}
            ]

            # Streaming completion
            stream = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield json.dumps({
                        "event": "chunk",
                        "data": chunk.choices[0].delta.content
                    })

            # Final done event
            yield json.dumps({"event": "done"})

        except Exception as e:
            logging.error(f"Error generating streaming response with OpenRouter: {e}")
            yield json.dumps({
                "event": "chunk",
                "data": "Sorry, I encountered an error processing your request."
            })
            yield json.dumps({"event": "done"})

    async def check_connection(self) -> bool:
        """Async wrapper to check connection"""
        return self.is_connected
