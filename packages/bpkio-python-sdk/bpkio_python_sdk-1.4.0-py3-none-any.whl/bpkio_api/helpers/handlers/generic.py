import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests

from bpkio_api.defaults import USER_AGENT_FOR_HANDLERS
from bpkio_api.exceptions import BroadpeakIoHelperError


class ContentHandler(ABC):
    content_types = []
    file_extensions = []

    document = None

    @abstractmethod
    def __init__(
        self, url, content: Optional[bytes] = None, user_agent: Optional[str] = None
    ):
        self.logger = logging.getLogger("bpkio_api.content_handler")

        self.url = url
        self.original_url = url
        if content:
            self._content = content
        else:
            self._content = None

        self.headers = {"User-Agent": user_agent or USER_AGENT_FOR_HANDLERS}

        # broadpeak session id (in case handler is for a bpk sessionservice)
        self.session_id = None

    @property
    def content(self):
        if self._content is None:
            self._fetch_content()
        return self._content

    def _fetch_content(self) -> bytes:
        self.logger.debug(
            f"Fetching content from {self.url} with headers {self.headers}"
        )
        response = requests.get(self.url, headers=self.headers)
        self._content = response.content

        # overwrite the URL, in case of redirect
        self.url = response.url

        # check if a broadpeak.io session was started
        params = parse_qs(
            urlparse(self.url).query, keep_blank_values=True, strict_parsing=False
        )
        if "sessionid" in params:
            self.session_id = params["sessionid"][0]

        return self._content

    @staticmethod
    def fetch_content_with_size_limit(
        url, size_limit, headers, enforce_limit=True, timeout=5
    ):
        response = requests.get(url, stream=True, headers=headers)  # , timeout=timeout)
        if response.status_code != 200:
            raise BroadpeakIoHelperError(
                status_code=response.status_code,
                message="Unable to fetch content - "
                + f"server response {response.status_code} for url {url}",
                original_message="",
            )

        content = b""
        for chunk in response.iter_content(chunk_size=1024):
            content += chunk
            if len(content) > size_limit:
                raise Exception("Content too long to be parseable efficiently")
        return content

    def reload(self):
        self._fetch_content()

    @staticmethod
    @abstractmethod
    def is_supported_content(content) -> bool:
        pass

    def has_children(self) -> bool:
        return False

    def get_child(self, index: int) -> "ContentHandler | None":
        return None

    @abstractmethod
    def read(self):
        pass

    def extract_info(self) -> Dict | None:
        return None

    def extract_features(self) -> List[Dict] | None:
        return None
