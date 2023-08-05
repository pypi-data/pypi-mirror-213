import time
from http import HTTPStatus
from http.client import HTTPException

import click
from requests import request
from requests.adapters import Response

from tenyks.config.config import Config

API_MAX_RETRIES = 3


class Api:
    """
    Low level rest api to access backend server.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config.load()
        self.api_url = self.config.api_url
        self.username = self.config.username
        self.password = self.config.password
        self.__authenticate()

    def __authenticate(self):
        click.echo("Authenticating...")
        self.headers = self.get_authenticated_header()
        click.echo("Authentication successful.")

    def get_authenticated_header(self):
        self.headers = None  # init headers
        token = self.__get_bearer_token_for_credentials(self.username, self.password)
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    def __get_bearer_token_for_credentials(self, username: str, password: str) -> str:
        payload = {"username": username, "password": password}

        response = self.post("/users/login", body=payload)
        return response["access_token"]

    def get(self, endpoint, params=None):
        """
        Generic GET Request Wrapper.
        """
        return self._api_request("GET", endpoint, headers=self.headers, params=params)

    def post(self, endpoint, body=None, files=None, data=None):
        """
        Generic POST Request Wrapper.
        """
        return self._api_request(
            "POST",
            endpoint,
            headers=self.headers,
            body=body,
            files=files,
            data=data,
        )

    def put(self, endpoint, body=None, files=None, data=None):
        """
        Generic POST Request Wrapper.
        """
        return self._api_request(
            "PUT",
            endpoint,
            headers=self.headers,
            body=body,
            files=files,
            data=data,
        )

    def delete(self, endpoint, params=None):
        """
        Generic DELETE Request Wrapper.
        """
        return self._api_request(
            "DELETE", endpoint, headers=self.headers, params=params
        )

    def _api_request(
        self,
        method,
        endpoint,
        headers=None,
        params=None,
        body=None,
        files=None,
        data=None,
        attempt=0,
    ):
        """
        Generic HTTP request method with error handling.
        """

        url = f"{self.api_url}{endpoint}"

        res = self._http_request(method, url, headers, params, body, files, data)

        json = None
        if res.status_code == HTTPStatus.UNAUTHORIZED and attempt < API_MAX_RETRIES:
            self.__authenticate()
            time.sleep((attempt + 1) ** 2)
            return self._api_request(
                method, endpoint, self.headers, params, body, files, data, attempt + 1
            )

        if res.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            json = res.json()
        elif res.status_code == HTTPStatus.NO_CONTENT.value:
            pass
        else:
            self._raise_on_response(res)

        return json

    def _http_request(
        self,
        method,
        url,
        headers=None,
        params=None,
        body=None,
        files=None,
        data=None,
    ) -> Response:
        """
        Generic HTTP Request Wrapper.
        """
        try:
            params = params or {}
            body = body or None

            res = request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=body,
                files=files,
                data=data,
            )

            return res
        except Exception as err:
            raise HTTPException(f"Failed {method} request to {url}. {err}")

    def _raise_on_response(self, res: Response):
        """
        Raise error on response.

        Args:
            res (Response): The response

        Raises:
            TenyksException: The TenyksException raised
        """
        try:
            json_error = res.json()
            message = json_error.get("message", res.text)
        except ValueError:
            message = res.text

        raise HTTPException(
            f"({res.status_code}) from {res.request.url}\nError message: {message} "
        )
