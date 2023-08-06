import asyncio
from typing import AsyncIterator, Generic, Optional, TypeVar

T = TypeVar("T")


class Link(Generic[T]):
    def __init__(self):
        self.item: Optional[T] = None
        self.next: Link = None


class Broadcast(Generic[T]):
    def __init__(self):
        self.current_link: Link[T] = Link()
        self.updated = asyncio.Event()

    def __aiter__(self) -> AsyncIterator[T]:
        return Iterator(self)

    def put_nowait(self, item: T):
        self.current_link.item = item
        self.current_link.next = Link()
        self.current_link = self.current_link.next
        self.updated.set()
        self.updated = asyncio.Event()

    def close(self):
        self.updated.set()


class Iterator(AsyncIterator[T]):
    def __init__(self, queue: Broadcast[T]):
        self.queue: Broadcast[T] = queue
        self.link: Link[T] = queue.current_link

    async def __anext__(self) -> T:
        if self.link.next is None:
            await self.queue.updated.wait()
        if self.link.next is None:
            raise StopAsyncIteration
        item = self.link.item
        self.link = self.link.next
        return item
