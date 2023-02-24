from app.services.httpx_client import HttpxClient
import httpx


async def test_httpx_client(mocker):
    mock_requests = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=httpx.Response(200, json={"token": "token"}),
    )
    mock_response = mocker.patch(
        "httpx.Response.raise_for_status",
    )

    mock = HttpxClient(base_url="http://testserver")
    assert mock._cli().base_url == "http://testserver"
    response = await mock.get('')
    mock_requests.assert_called()
    mock_response.assert_called()
