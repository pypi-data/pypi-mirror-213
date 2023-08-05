from asyncio.locks import BoundedSemaphore
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from types_aiobotocore_s3.client import S3Client


class AsyncS3ClientPool:
    """simple pool for async s3 resources"""

    async def open(self, n: int):
        self.session = get_session()

        self.free_clients: list[S3Client] = []
        for _ in range(n):
            client = await self.session.create_client("s3").__aenter__()
            self.free_clients.append(client)
        self.client_sema = BoundedSemaphore(n)

    async def close(self):
        for client in self.free_clients:
            await client.__aexit__(None, None, None)
        self.free_clients = []

    @asynccontextmanager
    async def s3_client(self) -> AsyncGenerator[S3Client, None]:
        async with self.client_sema:
            client = self.free_clients.pop()

            try:
                yield client
            finally:
                self.free_clients.append(client)


s3_pool = AsyncS3ClientPool()
