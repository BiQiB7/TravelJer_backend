from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Union
from PIL import Image

class BaseChatModel(ABC):
    """
    Abstract base class for a chat model, defining the interface for sending messages
    and handling responses.
    """

    @abstractmethod
    def send_message(self, messages: List[Union[str, Image.Image]]) -> Tuple[str, List[Image.Image], str]:
        """
        Sends a message to the chat model and processes the response.

        Args:
            messages: A list of messages to send to the model. Each message can be
                      a string or a PIL Image.

        Returns:
            A tuple containing the text response, a list of PIL Images, and the
            extension of the returned images.
        """
        pass