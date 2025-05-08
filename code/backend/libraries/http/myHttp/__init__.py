import aiohttp
import requests
from aiohttp import ClientResponse
from requests import Response


def post(url, json, headers=None) -> Response:
    return requests.post(url, json=json, headers=headers)


async def a_post(url, json, headers=None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json, headers=headers) as response:
            return response


def get(url, headers=None) -> Response:
    return requests.get(url, headers=headers)


async def a_get(url, headers=None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response


def delete(url, headers=None) -> Response:
    return requests.delete(url, headers=headers)


async def a_delete(url, headers=None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            return response


def put(url, json, headers=None) -> Response:
    return requests.put(url, json=json, headers=headers)


async def a_put(url, json, headers=None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=json, headers=headers) as response:
            return response
