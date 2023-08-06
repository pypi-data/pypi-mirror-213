from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (Any, AsyncGenerator, Dict, Generic, Iterable, List,
                    Literal, Optional, TypeVar, Union, cast)

from aiohttp import ClientSession

T = TypeVar("T")


class LazyProxy(Generic[T], ABC):
    def __init__(self) -> None:
        self.__proxied: T | None = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...




Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Json = Union[Dict[str, Any], List[Dict[str, Any]]]
MaybeJson = Optional[Json]
Headers = Dict[str, str]
MaybeHeaders = Optional[Headers]
CurrentSession = Optional[Union[ClientSession, LazyProxy[ClientSession]]]


class ApiClient(LazyProxy[ClientSession]):
    """

    Generic HTTP Client

    """
     
    def __load__(self) -> ClientSession:
        return ClientSession()

    async def fetch(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> MaybeJson:
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                try:
                    data = await response.json()
                    return data
                except (
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:
                    return None
                
    async def text(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> Optional[str]:
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                try:
                    data = await response.text()
                    return data
                except (
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:
                    return None
                
    async def stream(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> AsyncGenerator[str, None]:
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                async for chunk in response.content.iter_chunked(1024):
                    yield chunk.decode()
                    
    