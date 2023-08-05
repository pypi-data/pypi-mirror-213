from typing import Any
import aiohttp
import ujson
import ast


class Request:
    baseurl: str

    async def __call__(
            self,
            method: str, url: str,
            *,
            evaluate: bool = False,
            **kwargs
    ) -> Any:
        # convert params values to str
        if params := kwargs.get('params'):
            for key, value in params.items():
                kwargs['params'][key] = str(value)
        # assure that `method` supports
        assert (method := method.lower()) in ('get', 'post', 'put', 'delete')
        # request
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with getattr(session, method)(
                    await self.__url(url, kwargs['nobase']),
                    json=kwargs['body'],
                    params=kwargs['params'],
                    headers=kwargs['headers'],
                    data=kwargs['data']
            ) as response:
                try:
                    json = await response.json()
                    if evaluate:
                        json = self.__evaluate(json)
                    return json
                except Exception:
                    raise ValueError(await response.text())

    async def get(
            self,
            url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            nobase: bool = False
    ) -> Any:
        return await self('get', url, params=params, headers=headers, body=body, data=data, nobase=nobase)

    async def post(
            self,
            url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            nobase: bool = False
    ) -> Any:
        return await self('post', url, params=params, headers=headers, body=body, data=data, nobase=nobase)

    async def put(
            self,
            url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            nobase: bool = False
    ) -> Any:
        return await self('put', url, params=params, headers=headers, body=body, data=data, nobase=nobase)

    async def delete(
            self,
            url: str,
            *,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
            body: dict[str, Any] = None,
            data: dict[str, Any] = None,
            nobase: bool = False
    ) -> Any:
        return await self('delete', url, params=params, headers=headers, body=body, data=data, nobase=nobase)

    async def __url(self, url: str, nobase: bool = False):
        if not (base := self.baseurl) or nobase:
            return url
        if base.endswith('/') and url.startswith('/'):
            return base[:-1] + url
        elif base.endswith('/') and not url.startswith('/'):
            return base + url
        elif not base.endswith('/') and url.startswith('/'):
            return base + url
        elif not base.endswith('/') and not url.startswith('/'):
            return f'{base}/{url}'

    async def __evaluate(self, json: dict[str, Any]):
        # evaluate str repr of uuid to uuid, "b''" to b'' and so on
        def evaluate(value: bytes) -> Any:
            try:
                return ast.literal_eval(value.decode())
            except ValueError:
                return ast.literal_eval(f'\'{value.decode()}\'')
            except SyntaxError:
                return value.decode()
            except AttributeError:
                return None
        for key, value in json:
            json[key] = evaluate(value)
        return json


request = Request()
