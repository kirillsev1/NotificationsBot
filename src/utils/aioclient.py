from typing import AsyncGenerator

from aiohttp import ClientSession


async def get_client_session() -> AsyncGenerator[ClientSession, None]:
    async with ClientSession() as session:
        yield session
