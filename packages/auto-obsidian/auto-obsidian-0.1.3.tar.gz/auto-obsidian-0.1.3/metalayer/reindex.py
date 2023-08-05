import json
import os.path
import time
from datetime import datetime
from glob import glob
from multiprocessing import Queue

import sys
sys.path.append('..')
from metalayer import CAPTURE_DIR
from metalayer.consumer import CaptureConsumer


def index_captures(queue):
    for timestamp in sorted(os.listdir(CAPTURE_DIR)):
        windows = []
        try:
            dt = datetime.strptime(timestamp, '%Y-%m-%d_%H-%M-%S-%f')
        except:
            continue
        for window_path in glob(CAPTURE_DIR + timestamp + '/*.json'):
            with open(window_path, 'r') as f:
                window = json.load(f)
                windows.append(window)
        queue.put(('parse', dt, windows))
        # time.sleep(1)
    queue.put(('stop'))


if __name__ == '__main__':
    buffer = Queue()
    index_captures(buffer)

    consumer = CaptureConsumer(buffer, 'macos', wait_for_power=False)
    consumer.start()
    consumer.join()
