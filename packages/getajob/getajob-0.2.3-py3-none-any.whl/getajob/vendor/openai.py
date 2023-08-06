from pydantic import BaseModel
import openai

from getajob.utils import string_to_bool
from getajob.config.settings import SETTINGS


class OpenAIAPISettings(BaseModel):
    OPENAI_API_KEY: str = SETTINGS.OPENAI_API_KEY
    MOCK_RESPONSES: bool = string_to_bool(SETTINGS.OPENAI_API_KEY)
    MODEL_ABILITY: int = int(SETTINGS.OPENAI_MODEL_ABILITY)
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
    def __init__(self, settings: OpenAIAPISettings = OpenAIAPISettings()):
        self.settings = settings
        openai.api_key = self.settings.OPENAI_API_KEY

    def send_request(self, model: str, prompt: str, max_tokens: int = 60):
        if self.settings.MOCK_RESPONSES:
            return MOCKED_RESPONSE
        return openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=self.settings.TEMPERATURE,
            max_tokens=max_tokens,
            top_p=self.settings.TOP_P,
            frequency_penalty=self.settings.FREQUENCY_PENALTY,
            presence_penalty=self.settings.PRESENCE_PENALTY,
        )

    def text_prompt(self, prompt: str, max_tokens: int = 100):
        response = self.send_request(
            model=self.settings.MODEL, prompt=prompt, max_tokens=max_tokens
        )
        return dict(response["choices"][0])["text"]  # type: ignore
