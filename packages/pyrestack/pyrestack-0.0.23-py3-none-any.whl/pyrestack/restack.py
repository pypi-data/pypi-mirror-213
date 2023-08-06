"""ReStack client."""
from aiohttp import ClientSession

from .decorator import api_request
from .models import ReStackApiResponse

class ReStack:
    """This class is used to get information from ReStack."""

    def __init__(self, session: ClientSession, base_url: str, username: str, password: str, verify_ssl=True) -> None:
        """Initialize"""
        self._base_url = base_url
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._session: ClientSession = session

    @api_request("/stack")
    async def async_get_stacks(self, **kwargs) -> ReStackApiResponse:
        """Get monitors from API."""
