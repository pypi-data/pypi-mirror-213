import typing
import contextlib
from interface import QueryProto, ReturnType
from connection_repository import ConnectionRepository

import asyncpg


@typing.final
class PoolRepository:
    """Repository for asnycpg pool."""

    def __init__(self, storage: asyncpg.Pool) -> None:
        self._storage: asyncpg.Pool = storage

    async def insert(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def select(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def delete(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    async def update(self, query: QueryProto[ReturnType]) -> ReturnType:
        raise NotImplementedError()

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator[ConnectionRepository]:
        async with self._storage.acquire() as connection:
            async with ConnectionRepository(storage=connection).transaction() as connection_repository:
                yield connection_repository
