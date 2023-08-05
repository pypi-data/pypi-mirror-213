import os
import openai

from getajob.utils import string_to_bool


class OpenAIAPISettings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MOCK_RESPONSES: bool = string_to_bool(os.getenv("OPENAI_MOCK_RESPONSES"))
    MODEL_ABILITY: int = int(os.getenv("UPGRADED_OPENAI_MODELS", 1))
    TEMPERATURE: float = 0.5
    TOP_P: float = 1.0
    FREQUENCY_PENALTY: float = 0.8
    PRESENCE_PENALTY: float = 0.0

    MODEL_ABILITY_DICT = {1: "text-curie-001", 2: "gpt-3.5-turbo", 3: "gpt-4"}
    MODEL = MODEL_ABILITY_DICT[MODEL_ABILITY]


MOCKED_RESPONSE = {
    "choices": [
        {
            "finish_reason": "length",
            "index": 0,
            "logprobs": None,
            "text": "mocked response",
        }
    ],
    "created": 1619798989,
    "id": "cmpl-2ZQ8Z9Z1X9X9Z",
    "model": "davinci:2020-05-03",
    "object": "text_completion",
}


class OpenAIAPI:
    def __init__(self):
        openai.api_key = OpenAIAPISettings.OPENAI_API_KEY

    def send_request(self, model: str, prompt: str, max_tokens: int = 60):
        if OpenAIAPISettings.MOCK_RESPONSES:
            return MOCKED_RESPONSE
        return openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=OpenAIAPISettings.TEMPERATURE,
            max_tokens=max_tokens,
            top_p=OpenAIAPISettings.TOP_P,
            frequency_penalty=OpenAIAPISettings.FREQUENCY_PENALTY,
            presence_penalty=OpenAIAPISettings.PRESENCE_PENALTY,
        )

    def text_prompt(self, prompt: str, max_tokens: int = 100):
        response = self.send_request(
            model=OpenAIAPISettings.MODEL, prompt=prompt, max_tokens=max_tokens
        )
        return dict(response["choices"][0])["text"]  # type: ignore

    @classmethod
    def generate_image_from_prompt(cls, prompt: str, size: str, num_images: int = 1):
        response = openai.Image.create(prompt=prompt, n=num_images, size=size)
        return response["data"][0]["url"]  # type: ignore
