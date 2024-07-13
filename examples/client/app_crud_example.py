"""Client: Simple App CRUD example.

This example demonstrates how to use the gptdb client to get, list apps.
Example:
    .. code-block:: python

        GPTDB_API_KEY = "gptdb"
        client = Client(api_key=GPTDB_API_KEY)
        # 1. List all apps
        res = await list_app(client)
        # 2. Get an app
        res = await get_app(client, app_id="bf1c7561-13fc-4fe0-bf5d-c22e724766a8")
"""
import asyncio

from gptdb.client import Client
from gptdb.client.app import list_app


async def main():
    # initialize client
    GPTDB_API_KEY = "gptdb"
    client = Client(api_key=GPTDB_API_KEY)
    res = await list_app(client)
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
