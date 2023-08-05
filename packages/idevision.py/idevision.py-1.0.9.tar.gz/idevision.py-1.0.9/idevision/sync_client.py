import imghdr
import time
import typing
from io import BytesIO

import requests

from .errors import (
    ApiError,
    Banned,
    InvalidRtfmLibrary,
    InvalidRtfsLibrary,
    InvalidToken,
    MaxRetryReached,
    NotFound,
    TagAlreadyAssigned,
)
from .responses import (
    CDNResponse,
    CDNStats,
    CDNUpload,
    RTFMResponse,
    RTFSResponse,
    XKCDComic,
    XKCDResponse,
)


class sync_client:

    def __init__(
        self,
        token: typing.Union[str, None] = None,
        *,
        retry: typing.Optional[int] = 5,
        url: str = "https://idevision.net/api/",
    ):
        self.token = token

        self.retry = int(retry)

        self.base_url = url.strip("/") + "/"

    def _request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})

        if self.token:
            headers["Authorization"] = self.token

        if not headers:
            headers = None

        for _ in range(self.retry):
            with requests.request(
                method, url, headers=headers or None, **kwargs
            ) as response:
                if response.status_code in [200, 201]:
                    try:
                        return response.json()
                    except:
                        return response
                elif response.status_code in [400, 500]:
                    raise ApiError(response.reason)
                elif response.status_code == 403:
                    raise Banned()
                elif response.status_code == 429:
                    wait = float(response.headers["ratelimit-retry-after"])
                    time.sleep(wait)
                    continue
                elif response.status_code == 401:
                    raise InvalidToken(response.reason)
                elif response.status_code == 404:
                    if method == "DELETE":
                        return response
                    raise NotFound
                elif response.status_code == 204:
                    return True

        raise MaxRetryReached(self.retry)

    def sphinxrtfm(
        self,
        location: str,
        query: str,
        *,
        show_labels: bool = False,
        label_labels: bool = False,
    ) -> RTFMResponse:
        """Index a sphinx library from the given url, then returns results based on the given `query`

        :param location: The location of the sphinx documentation
        :type location: str
        :param query: The query to search for
        :type query: str
        :param show_labels: Whether to return labels, defaults to False
        :type show_labels: bool, optional
        :param label_labels: Whether to label labels, defaults to False
        :type label_labels: bool, optional
        :raises InvalidRtfmLibrary: The provided location is not sphinx documentation
        :return: An RTFMResponse object
        :rtype: RTFMResponse
        """
        with requests.get(f"{location.removesuffix('/')}/objects.inv") as resp:
            if resp.status == 404:
                raise InvalidRtfmLibrary(location)

        response = self._request(
            "GET",
            f"{self.base_url}public/rtfm.sphinx",
            params={
                "location": location,
                "query": query,
                "show-labels": "true" if show_labels else "false",
                "label-labels": "true" if label_labels else "false",
            },
        )

        return RTFMResponse(response["nodes"], response["query_time"])

    def rustrtfm(self, crate: str, query: str) -> RTFMResponse:
        """Index a rust crate documentation from the given url and return results based on the given `query`

        :param crate: The url of the crate documentation
        :type crate: str
        :param query: The query to search for
        :type query: str
        :return: An RTFMResponse object
        :rtype: RTFMResponse
        """
        response = self._request(
            "GET",
            f"{self.base_url}public/rtfm.rustdoc",
            params={"location": crate, "query": query},
        )

        return RTFMResponse(response["nodes"], response["query_time"])

    def rtfs(
        self, library: str, query: str, *, source: typing.Optional[bool] = False
    ) -> RTFSResponse:
        """Index a given python source code and return links or the source given the provided query

        :param library: The library to search. Can be one of "twitchio", "wavelink", "discord.py", "discord.py-2" or "aiohttp"
        :type library: str
        :param query: The query to search for
        :type query: str
        :param source: Whether to return the source, defaults to False
        :type source: typing.Optional[bool], optional
        :raises InvalidRtfsLibrary: The provided library is not valid
        :return: An RTFSResponse object
        :rtype: RTFSResponse
        """
        if library == "dpy":
            library = "discord.py"
        if library == "dpy2":
            library = "discord.py-2"

        allowed = {"twitchio", "wavelink", "discord.py", "discord.py-2", "aiohttp"}

        if library not in allowed:
            raise InvalidRtfsLibrary(library, *allowed)

        response = self._request(
            "GET",
            f"{self.base_url}public/rtfs",
            params={
                "library": library,
                "query": query,
                "format": "links" if not source else "source",
            },
        )

        return RTFSResponse(response["nodes"], response["query_time"])

    def ocr(
        self,
        image: typing.Union[BytesIO, bytes],
        *,
        filetype: typing.Optional[str] = None,
    ) -> str:
        """Read text from an image

        :param image: The image to read
        :type image: typing.Union[BytesIO, bytes]
        :param filetype: The filetype, can be auto-detected if left blank
        :type filetype: typing.Optional[str], optional
        :return: The raw text that was read
        :rtype: str

        .. note ::
            This current model does not work well with dark backgrounds. Try inverting the image to get better results.

        """
        if isinstance(image, BytesIO):
            image = image.read()

        if not filetype:
            filetype = imghdr.what(image)

        response = self._request(
            "GET",
            f"{self.base_url}public/ocr",
            params={"filetype": filetype},
            data=image,
        )

        return response["data"].strip()

    def xkcd(self, query: str) -> XKCDResponse:
        """Search for an xkcd comic by name

        :param query: The query to search for
        :type query: str
        :return: An XKCDResponse object
        :rtype: XKCDResponse
        """
        response = self._request(
            "GET", f"{self.base_url}public/xkcd", params={"search": query}
        )

        return XKCDResponse(
            [
                XKCDComic(
                    node["num"],
                    node["posted"],
                    node["safe_title"],
                    node["title"],
                    node["alt"],
                    node["transcript"],
                    node["news"],
                    node["image_url"],
                    node["url"],
                )
                for node in response["nodes"]
            ],
            response["query_time"],
        )

    def xkcd_tag(self, tag: str, number: int):
        """Add a tag to a specific xkcd comic

        :param tag: The string to add to the comic
        :type tag: str
        :param number: The number comic to add it to
        :type number: int
        :raises TagAlreadyAssigned: If the tag provided is already assigned
        """
        response = self._request(
            "PUT", f"{self.base_url}public/xkcd/tags", json={"tag": tag, "num": number}
        )

        if response.reason.startswith("Tag"):
            raise TagAlreadyAssigned(response.reason)

    def homepage(self, links: typing.Dict[str, str]):
        """Add links to your homepage, which can be viewed at https://idevision.net/homepage?user=YOUR_USERNAME

        :param links: A dictionary of str, str
        :type links: typing.Dict[str, str]
        :return: True if success
        :rtype: bool
        """
        return self._request("POST", f"{self.base_url}homepage", json=links)

    def cdn(
        self,
        image: typing.Union[BytesIO, bytes],
        *,
        filetype: typing.Optional[str] = None,
    ) -> CDNResponse:
        """Upload an image to the idevision cdn

        :param image: The image to upload
        :type image: typing.Union[BytesIO, bytes]
        :param filetype: The type of the image, can be detected if not specified
        :type filetype: typing.Optional[str], optional
        :return: A CDNResponse object
        :rtype: CDNResponse
        """
        if isinstance(image, BytesIO):
            image = image.read()

        if not filetype:
            filetype = imghdr.what(image)

        response = self._request(
            "POST", f"{self.base_url}cdn", headers={"File-Name": filetype}, data=image
        )

        return CDNResponse(response["url"], response["slug"], response["node"])

    def cdn_stats(self) -> CDNStats:
        """Return the current CDN stats

        :return: A CDNStats object
        :rtype: CDNStats
        """
        response = self._request("GET", f"{self.base_url}cdn")

        return CDNStats(
            response["upload_count"],
            response["uploaded_today"],
            response["last_upload"],
        )

    def cdn_get(self, node: str, slug: str) -> CDNUpload:
        """Get info on a cdn upload

        :param node: The node to search on
        :type node: str
        :param slug: The filename to search
        :type slug: str
        :return: A CDNUpload object
        :rtype: CDNUpload
        """
        response = self._request("GET", f"{self.base_url}cdn/{node}/{slug}")

        return CDNUpload(
            response["url"],
            response["timestamp"],
            response["author"],
            response["views"],
            response["node"],
            response["size"],
            response["expiry"],
        )

    def cdn_delete(self, node: str, slug: str) -> requests.Response:
        """Delete an entry to the cdn

        :param node: The node to search on
        :type node: str
        :param slug: The filename to search for
        :type slug: str
        :return: A requests.Response object
        :rtype: requests.Response
        """
        return self._request("DELETE", f"{self.base_url}cdn/{node}/{slug}")
