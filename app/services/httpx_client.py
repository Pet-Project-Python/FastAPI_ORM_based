import httpx


class HttpxClient:  # noqa: WPS214
    """Async client for HTTP requests."""

    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url
        self.timeout = 20

    async def get(
        self,
        url: str,
        query_params: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        return await self._request("GET", url, query_params=query_params, headers=headers)

    async def post(self, url: str, json: dict, headers: dict | None = None) -> httpx.Response:
        return await self._request("POST", url, json=json, headers=headers)

    async def _request(  # noqa: WPS211
        self,
        method: str,
        url: str,
        query_params: dict | None = None,
        json: dict | None = None,
        form_data: dict | None = None,
        headers: dict | None = None,
    ):
        async with self._cli() as cli:
            response: httpx.Response = await cli.request(
                method=method,
                url=url,
                params=query_params,
                json=json,
                data=form_data,
                headers=headers,
            )
            response.raise_for_status()
            return response

    def _cli(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        )
