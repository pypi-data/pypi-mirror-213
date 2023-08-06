import typing
import contextlib
from interface import QueryProto, ReturnType


@typing.final
class VCRStorage:
    """A fake repository storage which is used to pre-record database responses for queries."""

    _records: list[tuple[QueryProto[typing.Any], typing.Any]] = []

    def write(self, query: QueryProto[ReturnType], response: ReturnType) -> None:
        self._records.append((query, response))

    def read(self, query: QueryProto[ReturnType]) -> ReturnType:
        caller_frame: typing.Any = inspect.currentframe().f_back.f_back  # type: ignore
        line: str = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"

        if self._records == []:
            raise ValueError(
                f"FakeStorage.read: Failed to find a pre-recorded response for query for line {line}:\n"
                f"Expected: {query}\n"
            )

        recorded_query, recorded_response = self._records.pop(0)

        if query != recorded_query:
            raise ValueError(
                f"FakeStorage.read: Order of pre-recorded responses is messed up for line {line}:\n"
                f"Expected: {query}\n"
                f"Got: {recorded_query}\n"
            )

        return typing.cast(ReturnType, recorded_response)


@typing.final
class VCRRepository:
    """Repository that uses pre-recorded reponses for queries."""
    # TODO: Add link to VCR doc/examples.

    def __init__(self, storage: VCRStorage) -> None:
        self._storage = storage

    async def insert(self, query: QueryProto[ReturnType]) -> ReturnType:
        return self._storage.read(query)

    async def select(self, query: QueryProto[ReturnType]) -> ReturnType:
        return self._storage.read(query)

    async def delete(self, query: QueryProto[ReturnType]) -> ReturnType:
        return self._storage.read(query)

    async def update(self, query: QueryProto[ReturnType]) -> ReturnType:
        return self._storage.read(query)

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator["VCRRepository"]:
        try:
            yield VCRRepository(storage=self._storage)
        finally:
            pass
