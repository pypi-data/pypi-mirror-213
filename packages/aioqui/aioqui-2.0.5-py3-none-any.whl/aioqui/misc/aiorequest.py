from aiohttp import ClientSession
from typing import Any
import ujson


class Request:
    baseurl: str

    async def __call__(
            self,
            method: str, url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            nobase: bool = False,
            pythonize: bool = False
    ) -> Any:
        if params:  # convert params values to str
            params = {key: str(value) for key, value in params.items()}
        if (method := method.lower()) not in ('get', 'post', 'put', 'delete'):
            raise NotImplementedError(f'method: {method} is not supported by `aiorequest.request`')
        async with ClientSession(json_serialize=ujson.dumps) as session:
            async with getattr(session, method)(
                    await self.__url(url, nobase),
                    json=body, params=params, headers=headers, data=data
            ) as response:
                json = await response.json()
                if pythonize:
                    json = self.pythonize(json)
                return json

    async def get(self, url: str, **kwargs) -> Any:
        return await self('get', url, **kwargs)

    async def post(self, url: str, **kwargs) -> Any:
        return await self('post', url, **kwargs)

    async def put(self, url: str, **kwargs) -> Any:
        return await self('put', url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Any:
        return await self('delete', url, **kwargs)

    async def __url(self, url: str, nobase: bool = False):
        if not (base := self.baseurl) or nobase:
            return url
        if base.endswith('/') and url.startswith('/'):
            return base[:-1] + url
        if base.endswith('/') and not url.startswith('/'):
            return base + url
        if not base.endswith('/') and url.startswith('/'):
            return base + url
        # if not base.endswith('/') and not url.startswith('/'):
        return f'{base}/{url}'

    @staticmethod
    def convert(value: Any):
        from contextlib import suppress
        from ast import literal_eval
        from dateutil import parser
        from uuid import UUID

        # 'ed38fe7a-11e6-4c59-ac31-ef30848e8e83' to UUID('ed38fe7a-11e6-4c59-ac31-ef30848e8e83')
        with suppress(Exception):
            return UUID(value)
        # '2023-06-09 21:52:49.072155' to datetime.datetime(2023, 6, 9, 21, 52, 49, 72155)
        with suppress(Exception):
            return parser.parse(value)
        # (1, 1.1, True) remains as it is
        if isinstance(value, (int, float, bool)):
            return value
        # "b'bytes'" to b'bytes'
        with suppress(Exception):
            return literal_eval(value)
        # 'string' remains as it is
        if isinstance(value, str):
            return value
        # 'null' to None
        return None

    @staticmethod
    def pythonize(json: dict[Any, Any] | list[Any, ...]) -> dict[Any, Any] | list[Any, ...]:
        # handles dict
        if isinstance(json, dict):
            return {key: Request.pythonize(value) for key, value in json.items()}
        # handles list
        if isinstance(json, list):
            return [Request.pythonize(element) for element in json]
        # converts the value
        return Request.convert(json)


request = Request()
