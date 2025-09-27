import io
import os
from typing import Any, List, Tuple, Union

from dotenv import load_dotenv
from google import genai
from PIL import Image

from .base import BaseChatModel

load_dotenv()
class GoogleGenAIChatModel(BaseChatModel):
    """
    A chat model implementation for the Google GenAI API.
    """

    def __init__(self, model_name: str = 'gemini-2.5-flash', api_key: str = None):
        """
        Initializes the GoogleGenAIChatModel.

        Args:
            model_name: The name of the model to use.
            api_key: The Google API key. If not provided, it will be read from
                     the GOOGLE_API_KEY environment variable.
        """
        if api_key is None:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set.")
        self.model =  genai.Client(api_key=api_key)
        self.chat = self.model.chats.create(model=model_name)        
        # genai.configure(api_key=api_key)
        # self.model = genai.GenerativeModel(model_name)

    def send_message(self, messages: List[Union[str, Image.Image]]) -> Tuple[str, List[Image.Image], str]:
        """
        Sends a message to the Google GenAI model and processes the response.

        Args:
            messages: A list of messages to send to the model.

        Returns:
            A tuple containing the text response, a list of PIL Images, and the
            extension of the returned images.
        """
        print(messages)
        response = self.chat.send_message(messages)
        print(response)
        return self._process_response(response)

    def get_history(self) -> List[Any]:
        """
        This model is now stateless, so it does not maintain history.
        """
        return []

    def _process_response(self, response: Any) -> Tuple[str, List[Image.Image], str]:
        """
        Processes a GenerateContentResponse, extracting text and images.

        Args:
            response: The GenerateContentResponse object from the model.

        Returns:
            A tuple containing the text response, a list of PIL Images, and the
            extension of the returned images.
        """
        text_response = ""
        images = []
        extension = None

        for part in response.parts:
            if hasattr(part, 'text') and part.text:
                text_response += part.text
            elif hasattr(part, 'inline_data') and part.inline_data:
                blob = part.inline_data
                mime_type = blob.mime_type
                image_data = blob.data

                if 'png' in mime_type:
                    extension = '.png'
                elif 'jpeg' in mime_type or 'jpg' in mime_type:
                    extension = '.jpg'
                else:
                    extension = '.bin'
                
                image_bytes_io = io.BytesIO(image_data)
                pil_image = Image.open(image_bytes_io)
                images.append(pil_image)

        return text_response, images, extension