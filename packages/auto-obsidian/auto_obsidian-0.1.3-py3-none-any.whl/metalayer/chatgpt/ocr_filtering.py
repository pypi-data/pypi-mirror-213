from metalayer.chatgpt import complete, complete_async
from metalayer.chatgpt.utils import load_prompts, fill_messages, retry_on_exception


system_prompt, user_prompt = load_prompts('ocr_filtering')

completion_params = {
    'model': 'gpt-3.5-turbo',
    'temperature': 0,
}


def filter_text(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    filtered = complete(messages, **completion_params)
    return filtered


@retry_on_exception(retries=5, initial_wait_time=1)
async def filter_text_async(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    filtered = await complete_async(messages, **completion_params)
    return filtered
