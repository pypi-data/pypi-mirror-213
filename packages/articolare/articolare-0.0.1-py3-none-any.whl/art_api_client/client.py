import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging


class ArticolareClient:
    BASE_URL = "https://articolare-translator-api-yr2dhc67qa-uc.a.run.app/"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}"
        })

        # Set up retry mechanism
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.BASE_URL}/{endpoint}"
        logging.info(f"Making a {method} request to {url} with {kwargs}")
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
        else:
            logging.info(f"Received a response: {response.json()}")
            return response.json()

    def create(self, model, lang, style, prompt, max_tokens):
        """
        Create a new request with the specified model, language, style, prompt, and maximum tokens.

        Parameters:
        model (str): The model to use.
        lang (str): The target language for translation (English, Portuguese, Spanish, or Italian).
        style (str): The style of translation (conversation, formal, or informal).
        prompt (str): The prompt to complete.
        max_tokens (int): The maximum number of tokens in the response.

        Returns:
        dict: The response data.

        Raises:
        requests.HTTPError: If the API request fails.
        """
        if not isinstance(model, str):
            raise TypeError("model must be a string.")
        if lang not in ["English", "Portuguese", "Spanish", "Italian"]:
            raise ValueError("Invalid language. Supported languages are English, Portuguese, Spanish, or Italian.")
        if style not in ["conversation", "formal", "informal"]:
            raise ValueError("Invalid style. Supported styles are conversation, formal, or informal.")
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string.")
        if not isinstance(max_tokens, int):
            raise TypeError("max_tokens must be an integer.")

        data = {
            "model": model,
            "lang": lang,
            "style": style,
            "prompt": prompt,
            "max_tokens": max_tokens
        }

        return self._request("POST", "create", json=data)



