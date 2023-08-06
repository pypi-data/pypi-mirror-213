import abc
import typing
import contextlib


# TODO: Docs.
ReturnType = typing.TypeVar("ReturnType")

class QueryProto(typing.Generic[ReturnType], typing.Protocol):
    """TODO: Docs."""
    query: str
    values: tuple[typing.Any, ...]
    return_type: typing.Type[ReturnType]


class SQLRepositoryProto(typing.Protocol):
    """Interface for SQL repositories."""

    @abc.abstractmethod
    async def insert(self, query: QueryProto[ReturnType]) -> ReturnType:
        """Insert a new record into storage."""

    @abc.abstractmethod
    async def select(self, query: QueryProto[ReturnType]) -> ReturnType:
        """Select records or their meta information (fields, count) from the storage."""

    @abc.abstractmethod
    async def delete(self, query: QueryProto[ReturnType]) -> ReturnType:
        """Delete record from the storage."""

    @abc.abstractmethod
    async def update(self, query: QueryProto[ReturnType]) -> ReturnType:
        """Update existing record in the storage."""

    # TODO: Allow to pass transaction parameters.
    @abc.abstractmethod
    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator["SQLRepositoryProto"]:
        """TODO"""
        raise NotImplementedError
        yield None  # Mypy requires this line to properly determine type.
