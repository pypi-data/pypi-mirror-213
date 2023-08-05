import asyncio
import json

import requests
import aiohttp

from metalayer.chatgpt.logger import log_result, log_result_async

SERVER_URL = 'https://openai-server-smh3yefbia-ue.a.run.app/complete'


@log_result
def complete(messages, model='gpt-3.5-turbo', **completion_kwargs):
    data = {
        'messages': messages,
        'model': model,
        **completion_kwargs,
    }
    response = requests.post(SERVER_URL, json=data)
    text = json.loads(response.text)
    status = response.status_code
    if status != 200:
        raise Exception(f'Error {status} from server: {text}')
    return text


@log_result_async
async def complete_async(messages, model='gpt-3.5-turbo', **completion_kwargs):
    async with aiohttp.ClientSession() as session:
        data = {
            'messages': messages,
            'model': model,
            **completion_kwargs,
        }
        async with session.post(SERVER_URL, json=data) as response:
            text = await response.text()
            text = json.loads(text)
            status = response.status
            if status != 200:
                raise Exception(f'Error {status} from server: {text}')
            return text


if __name__ == '__main__':
    messages = [{'role': 'system', 'content': "What's 2+2?"}]
    model = 'gpt-3.5-turbo'
    print(complete(messages, model))
    print('*' * 80)
    print(asyncio.run(complete_async(messages, model)))
