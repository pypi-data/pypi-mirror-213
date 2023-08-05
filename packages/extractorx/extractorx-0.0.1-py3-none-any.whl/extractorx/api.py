import json
from typing import Optional, Union
import urllib3

import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ExtractorX(object):
    """
    Python Wrapper for ExtractorX API
    """
    def __init__(self, key: str):
        if not isinstance(key, str):
            raise ValueError("'key' must be a string.")
        self.key = key
        self.api_endpoint = "https://extractorx.com/api"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _call_api(self, data: dict) -> dict:
        r = requests.post(
            self.api_endpoint,
            headers=self.headers,
            data=json.dumps(data),
            verify=False
        )
        return r.json()

    def _check_confidence(self, confidence: Union[float, None]) -> None:
        if confidence is None:
            return
        if not isinstance(confidence, float):
            raise ValueError("'confidence' must be a float")
        if not (0. < confidence < 1.):
            raise ValueError("'confidence' must be between 0 and 1")

    def from_url(self, url: str, confidence: Optional[float] = None) -> dict:
        if not isinstance(url, str):
            raise ValueError("'url' must be a string")
        self._check_confidence(confidence)
        data = {"key": self.key, "url": url, "confidence": confidence}
        return self._call_api(data)

    def from_html(self, html: str, confidence: Optional[float] = None) -> dict:
        if not isinstance(html, str):
            raise ValueError("'html' must be a string")
        self._check_confidence(confidence)
        data = {"key": self.key, "body": html, "confidence": confidence}
        return self._call_api(data)
