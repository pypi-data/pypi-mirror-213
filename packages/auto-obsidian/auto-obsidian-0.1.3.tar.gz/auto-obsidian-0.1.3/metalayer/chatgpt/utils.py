import os

from metalayer import METALAYER_PATH


def load_prompts(task_identifier):
    prompt_path = os.path.join(METALAYER_PATH, f'chatgpt/prompts/{task_identifier}/')
    system_path = prompt_path + 'system.txt'
    user_path = prompt_path + 'user.txt'

    system_prompt = None
    user_prompt = None
    if os.path.exists(system_path):
        with open(system_path, 'r') as f:
            system_prompt = f.read()
    if os.path.exists(user_path):
        with open(user_path, 'r') as f:
            user_prompt = f.read()
    return system_prompt, user_prompt


def fill_messages(system_prompt, user_prompt, *args):
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    if user_prompt:
        if len(args) > 0:
            user_prompt = user_prompt.format(*args)
        messages.append({'role': 'user', 'content': user_prompt})
    return messages


def get_response_text(response):
    text = response.choices[0].message.content
    return text.encode("ascii", errors="ignore").decode()


import asyncio
def retry_on_exception(retries=5, initial_wait_time=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            wait_time = initial_wait_time
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        raise e
                    print(e)
                    await asyncio.sleep(wait_time)
                    wait_time *= 2
        return wrapper
    return decorator
