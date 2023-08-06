import os
import requests
from ratelimiter import RateLimiter

VERSION = "v1"


class BoundlessAIBase:
    def __init__(self) -> None:
        self.api_key = os.getenv("BOUNDLESS_AI_API_KEY")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        self.base_url = f"https://api.boundlessai.io/{VERSION}"

    def get_account_id(self) -> str:
        """Get the account ID."""
        url = f"{self.base_url}/account"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return response.json()["id"]


class Chatbot(BoundlessAIBase):
    def __init__(self, chatbot_id: str) -> None:
        super().__init__()
        self.chatbot_id = chatbot_id

    @RateLimiter(max_calls=10, period=60)
    def train(self, text: str) -> None:
        """Train the chatbot with a text string."""
        url = f"{self.base_url}/chatbots/{self.chatbot_id}/train"
        response = requests.post(url, json={"text": text}, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return None

    @RateLimiter(max_calls=100, period=60)
    def interact(self, text: str) -> str:
        """Interact with the chatbot with a text string."""
        url = f"{self.base_url}/chatbots/{self.chatbot_id}/interact"
        response = requests.post(url, json={"question": text}, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return response.json()["response_text"]


class BoundlessAI(BoundlessAIBase):
    
    def __init__(self) -> None:
        super().__init__()

    @RateLimiter(max_calls=10, period=60)
    def get_chatbot(self, chatbot_id: str) -> dict:
        """Get a chatbot by ID.

        Args:
            chatbot_id (str): The chatbot ID.

        Returns:
            dict: The chatbot object.
        """
        return Chatbot(chatbot_id)
    
    @RateLimiter(max_calls=10, period=60)
    def create_chatbot(self, name: str, prompt: str = "") -> None:
        """Create a chatbot.

        Args:
            chatbot (dict): The chatbot object.

        Returns:
            dict: The chatbot object.
        """
        url = f"{self.base_url}/chatbots"
        chatbot = {
            "name": name,
            "prompt": prompt,
            "model": "gpt-3.5-turbo",
            "account_id": self.get_account_id(),
        }
        response = requests.post(url, json=chatbot, headers=self.headers)

        if response.status_code != 200:
            raise Exception(response.text)
        else:
             chatbot_id = response.json()["entity_id"]
             return Chatbot(chatbot_id)

    RateLimiter(max_calls=10, period=60)    
    def delete_chatbot(self, chatbot_id: str) -> None:
        """Delete a chatbot by ID.

        Args:
            chatbot_id (str): The chatbot ID.
        """
        url = f"{self.base_url}/chatbots/{chatbot_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return None
