import asyncio
import json
import os
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import Levenshtein

from metalayer import config, CAPTURE_DIR, ACTIVITY_LOG_DIR
from metalayer.auto_obsidian.graph import Graph as ObsidianGraph
from metalayer.chatgpt.activity_log import log_activity_async
from metalayer.ocr import OCR
from metalayer.system import battery
from metalayer.utils import timed


class CaptureConsumer(Thread):

    def __init__(self, buffer, ocr_engine, wait_for_power=True, fix_ocr=True):
        super().__init__()
        self.buffer = buffer
        self.ocr = OCR(ocr_engine, fix_ocr=fix_ocr)
        self.wait_for_power = wait_for_power
        self.text_cache = deque(maxlen=10)
        self.text_cache_lock = asyncio.Lock()
        self.executor = ThreadPoolExecutor()
        self.obsidian_vault_path = config.get('vault_dir')

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._run())

    async def _init_graph(self):
        self.obsidian_graph = None
        if self.obsidian_vault_path is not None:
            self.obsidian_graph = ObsidianGraph(self.obsidian_vault_path)

    async def _run(self):
        # Init graph after setting event loop, so locks share the same loop
        await self._init_graph()
        waiting = False
        tasks = []
        while True:
            if self.wait_for_power and battery.on_battery():
                if not waiting:
                    print('[INFO] Waiting for external power to run OCR...')
                    waiting = True
                await asyncio.sleep(1)
                continue

            waiting = False

            item = await self.loop.run_in_executor(None, self.buffer.get)
            action, *data = item
            if action == 'parse':
                datetime, windows = data
                for window in windows:
                    task = self.loop.create_task(self.process_window(datetime, window))
                    tasks.append(task)
                    await asyncio.sleep(0.1)
            elif action == 'stop':
                break

            tasks = [t for t in tasks if not t.done() and not t.cancelled()]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def process_window(self, datetime, window):
        window['time_string'] = datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
        res = await self.loop.run_in_executor(self.executor, self.extract_text, window)
        print('[INFO] Executor finished')
        if not res:
            return
        
        await self.process_text(window)


    @timed("[INFO] OCR completed in {:.2f} seconds")
    def extract_text(self, window):
        try:
            if 'ocr_results' not in window:
                window_crop = window.pop('screenshot')
                ocr_blocks = self.ocr(window_crop, paragraph=False)
                window['ocr_results'] = ocr_blocks
        except Exception as e:
            print('[ERROR] OCR Failed!')
            print(str(e))
            return False

        if len(window['ocr_results']) == 0:
            print('[INFO] No OCR results found')
            return False

        time_string = window['time_string']
        page_id = window['page_id']
        save_path = os.path.join(CAPTURE_DIR, time_string, page_id + '.json')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as f:
            json.dump(window, f)
        return True

    async def process_text(self, window):
        activity_log = await self.create_activity_log(window)

        if self.obsidian_graph is not None and activity_log is not None:
            print('[INFO] Inserting knowledge into Obsidian')
            await self.obsidian_graph.insert_knowledge(
                app=window['app'],
                title=window['title'],
                summary=activity_log['summary'],
                activity=activity_log['activity'],
                info=activity_log['info'],
                ocr_results=window['ocr_results'],
            )

    async def create_activity_log(self, window):
        ocr_blocks = window['ocr_results']
        page_id = window['page_id']
        time_string = window['time_string']

        text = '\n'.join(text for bbox, text in ocr_blocks)
        async with self.text_cache_lock:
            if self.check_cached_text(text):
                print('[INFO] Skipping chatgpt calls due to duplicate text')
                return

        try:
            print('[INFO] Creating activity log for page_id: {}'.format(page_id))
            activity_log = await log_activity_async(text)
        except Exception as e:
            print('[ERROR] OpenAIError during info extraction!')
            print(str(e))
            return

        print('[INFO] Activity log created for page_id: {}'.format(page_id))
        log_path = os.path.join(ACTIVITY_LOG_DIR, time_string, page_id + '.json')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as f:
            json.dump(activity_log, f, indent=4)

        return activity_log

    def check_cached_text(self, text):
        lines = text.split('\n')
        if len(lines) == 0:
            return False
        for prev_text in self.text_cache:
            num_matches = 0
            n = 0
            prev_lines = prev_text.split('\n')
            if not (0.8 < len(prev_lines) / len(lines) < 1/0.8):
                continue
            for line1 in prev_lines:
                for line2 in lines:
                    if Levenshtein.ratio(line1, line2) > 0.8:
                        num_matches += 1
                        break
                n += 1
            if num_matches / n > 0.8:
                return True
        self.text_cache.append(text)
        return False

if __name__ == '__main__':
    pass
