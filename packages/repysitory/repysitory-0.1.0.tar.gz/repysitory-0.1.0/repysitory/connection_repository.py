import typing
import contextlib
from interface import QueryProto, ReturnType
from connection_repository import ConnectionRepository

import asyncpg


@typing.final
class ConnectionRepository:
    """Connection repository for asyncpg."""

    def __init__(self, storage: asyncpg.Connection) -> None:
        self._storage: asyncpg.Connection = storage

    async def insert(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def select(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def delete(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def update(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator["ConnectionRepository"]:
        async with self._storage.transaction():
            yield self

