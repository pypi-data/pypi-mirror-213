from metalayer.chatgpt import complete, complete_async
from metalayer.chatgpt.utils import load_prompts, fill_messages, retry_on_exception


system_prompt, user_prompt = load_prompts('info_extraction')

completion_params = {
    'temperature': 0,
    'presence_penalty': 0.5,
    'frequency_penalty': 0.5,
    'stop': ['\n\n']
}

def extract_info(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    extracted = complete(messages, **completion_params)
    if extracted.startswith('- '):
        extracted = extracted[2:].replace('\n- ', '\n')
    return extracted


@retry_on_exception(retries=5, initial_wait_time=1)
async def extract_info_async(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    extracted = await complete_async(messages, **completion_params)
    if extracted.startswith('- '):
        extracted = extracted[2:].replace('\n- ', '\n')
    return extracted
