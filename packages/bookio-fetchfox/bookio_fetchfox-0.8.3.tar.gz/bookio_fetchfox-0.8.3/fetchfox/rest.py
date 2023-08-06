import asyncio
from typing import Tuple

import aiohttp
import backoff


@backoff.on_exception(backoff.expo, exception=Exception, max_time=60)
def get(
    url: str,
    headers: dict = None,
    params: dict = None,
    sleep: float = 0.05,
    timeout: float = None,
) -> Tuple[dict, int]:
    async def aux():
        client = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
        )

        await asyncio.sleep(sleep)

        async with client as session:
            async with session.get(
                url,
                headers=headers,
                params=params,
            ) as response:
                json = await response.json()
                status_code = response.status

            await response.release()

        return json, status_code

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(aux())
    loop.close()

    return result


@backoff.on_exception(backoff.expo, exception=Exception, max_time=60)
def post(
    url: str,
    body: dict = None,
    headers: dict = None,
    params: dict = None,
    sleep: float = 0.05,
    timeout: float = None,
) -> Tuple[dict, int]:
    async def aux():
        client = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
        )

        await asyncio.sleep(sleep)

        async with client as session:
            async with session.post(
                url,
                json=body,
                headers=headers,
                params=params,
            ) as response:
                json = await response.json()
                status_code = response.status

            await response.release()

        return json, status_code

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(aux())
    loop.close()

    return result
