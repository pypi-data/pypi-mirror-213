import os
from datetime import datetime

history_path = os.path.join(os.path.dirname(__file__), 'history/')
os.makedirs(history_path, exist_ok=True)

def log_result(func):
    def wrapper(*args, **kwargs):
        messages = args[0]
        result = func(*args, **kwargs)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        with open(os.path.join(history_path, f'{timestamp}.txt'), 'w') as f:
            for msg in messages:
                f.write(f'{msg["role"].upper()}:\n\n{msg["content"]}\n\n')
            f.write(f'ASSISTANT:\n\n{result}')
        return result
    return wrapper

def log_result_async(func):
    async def wrapper(*args, **kwargs):
        messages = args[0]
        result = await func(*args, **kwargs)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        with open(os.path.join(history_path, f'{timestamp}.txt'), 'w') as f:
            for msg in messages:
                f.write(f'{msg["role"].upper()}:\n\n{msg["content"]}\n\n')
            f.write(f'ASSISTANT:\n\n{result}')
        return result
    return wrapper
