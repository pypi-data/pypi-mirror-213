import asyncio
import httpx
import json
import aiofiles

class AsyncClient(): #非同期class async with文で利用できる。

    def __init__(self, host="127.0.0.1", port=50031):
        self.host = host
        self.port = port

    async def __aenter__(self):
        self.client = httpx.AsyncClient(base_url=f"http://{self.host}:{self.port}")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def generate(self, text, speaker, path):
        query = await self.client.post('/audio_query',params = {'text': text, 'speaker': speaker})
        response = await query.aread()
        synthesis = await self.client.post('/synthesis',params = {'speaker': speaker},data=response)
        async with aiofiles.open(path, mode='wb') as f:
            await f.write(synthesis.content)

class Client(): #同期Class with文で利用できる。

    def __init__(self, host="127.0.0.1", port=50031):
        self.host = host
        self.port = port

    def __enter__(self):
        self.client = httpx.Client(base_url=f"http://{self.host}:{self.port}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def generate(self, text, speaker, path):#
        query = self.client.post('/audio_query',params = {'text': text, 'speaker': speaker})
        synthesis = self.client.post('/synthesis',params = {'speaker': speaker},data=json.dumps(query.json()))
        with open(path, mode='wb') as f:
            f.write(synthesis.content)