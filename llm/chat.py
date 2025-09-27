import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import List, Union, Dict

from PIL import Image

from .base import BaseChatModel

class ChatManager:
    """
    A class for managing chat interactions with a multimodal LLM.
    It is model-agnostic and works with any model that implements the BaseChatModel interface.
    """

    def __init__(self, chat_model: BaseChatModel):
        """
        Initializes the ChatManager.

        Args:
            chat_model: An instance of a class that inherits from BaseChatModel.
        """
        self.chat_model = chat_model
        self.history: List[Dict[str, Union[str, Image.Image]]] = []

    def send_message(self, messages: List[Union[str, Image.Image]]):
        """
        Sends a message to the chat model and processes the response, maintaining history.

        Args:
            messages: A list of messages to send to the model.

        Returns:
            A tuple containing the text response, a list of PIL images, and image extension.
        """
        # Prepend history to the current message for context
        contextual_messages = [item["content"] for item in self.history] + messages
        
        text_response, images, extension = self.chat_model.send_message(contextual_messages)

        # Update history with the user's message and the model's response
        for message in messages:
            self.history.append({"role": "user", "content": message})
        
        if text_response:
            self.history.append({"role": "assistant", "content": text_response.replace("{","{{").replace("}","}}")})
        if images:
            for image in images:
                self.history.append({"role": "assistant", "content": image})
            
        return text_response, images, extension

    def get_history(self):
        """
        Returns the current chat history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the chat history.
        """
        self.history = []

    def parse_history_for_display(self):
        """
        Parses the chat history for display, converting images to base64 data URLs.

        Returns:
            A list of strings, where each string is either a text message or
            a base64 encoded data URL for an image.
        """
        parsed_history = []
        for item in self.history:
            content = item["content"]
            if isinstance(content, str):
                parsed_history.append({"text":content})
            elif isinstance(content, Image.Image):
                # buffered = io.BytesIO()
                # # Determine format, default to PNG
                # img_format = content.format if content.format else 'PNG'
                # content.save(buffered, format=img_format)
                # img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
                # mime_type = Image.MIME.get(img_format, 'image/png')
                # data_url = f"data:{mime_type};base64,{img_str}"
                # data_url
                parsed_history.append({"image_url":""})
        return parsed_history

if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_community.llms import Replicate
    from .google_chat import GoogleGenAIChatModel

    load_dotenv()

    # # --- Example with Google GenAI ---
    print("--- Testing Google GenAI Model ---")
    try:
        google_model = GoogleGenAIChatModel(model_name='gemini-2.5-flash-image-preview')
        chat_manager_google = ChatManager(chat_model=google_model)

        # First message
        # mask = Image.open("assets/20250918012456740129/segmentation/cutout/background_.png")
        mask = Image.open('assets/20250918062838571181/segmentation_An apple pie with a lattice crust, partially visible, on a transparent background./cutout/union_cutout.png')
        image = Image.open("src/llms/d0f0a191bf16ed2106e5292745b4584e.jpg")
        prompt="Imagine the missing part of the object being completed."
        # "Complete the missing part of the background."
        text_response, images, _ = chat_manager_google.send_message([mask, prompt])
        print(f"Response 1: {text_response}")
        images[0].save("1__.png")

    #     # Second message (with history)
        
    #     text_response, images, _ = chat_manager_google.send_message(["change pink color to orange color"])
    #     print(f"Response 2: {text_response}")
    #     images[0].save("2.png")
        
    #     print("\n--- Google GenAI History ---")
    #     print(chat_manager_google.parse_history_for_display())

    except Exception as e:
        print(f"Error with Google GenAI: {e}")


    # # --- Example with LangChain (Replicate) ---
    # print("\n--- Testing LangChain Model (Replicate) ---")
    # try:
        # Make sure to set REPLICATE_API_TOKEN in your .env file
    #     replicate_model = Replicate(
    #         model="replicate/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165d71",
    #         model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1}
    #     )
    #     langchain_model = LangChainChatModel(model=replicate_model)
    #     chat_manager_langchain = ChatManager(chat_model=langchain_model)

    #     # First message
    #     text_response, _, _ = chat_manager_langchain.send_message(["What is the capital of France?"])
    #     print(f"Response 1: {text_response}")

    #     # Second message (with history)
    #     text_response, _, _ = chat_manager_langchain.send_message(["And what is its population?"])
    #     print(f"Response 2: {text_response}")

    #     print("\n--- LangChain History ---")
    #     # Note: History display for LangChain will depend on the model's response format
    #     print(chat_manager_langchain.get_history())

    # except Exception as e:
    #     print(f"Error with LangChain/Replicate: {e}")

    # # --- Example with Replicate Image Model (seedream_4) ---
    # print("\n--- Testing Replicate Image Model (seedream_4) ---")
    # try:
    #     image_model = ReplicateImageChatModel(model_name="bytedance/seedream-4")
    #     chat_manager_image = ChatManager(chat_model=image_model)

    #     # Generate an image with a prompt
    #     _, images, _ = chat_manager_image.send_message(["A futuristic cityscape at sunset"])
    #     if images:
    #         print("Generated image 1:")
    #         # images[0].show()
    #         images[0].save("generated_image_1.png")

    #     # Generate another image, this time with an input image
    #     try:
    #         with Image.open("generated_image_1.png") as img:
    #             _, images, _ = chat_manager_image.send_message(["Make it nighttime", img])
    #             if images:
    #                 print("Generated image 2:")
    #                 # images[0].show()
    #                 images[0].save("generated_image_2.png")
    #     except FileNotFoundError:
    #         print("Skipping second image generation as 'generated_image_1.png' was not found.")

    # except Exception as e:
    #     print(f"Error with Replicate Image Model: {e}").