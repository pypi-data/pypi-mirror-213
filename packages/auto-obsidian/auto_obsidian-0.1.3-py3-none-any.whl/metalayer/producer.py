import os
import sys
sys.path.append('..')
sys.path.append('serialization/')

from datetime import datetime
from threading import Thread, Timer

from PIL import Image
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

from metalayer import THUMBNAIL_DIR
from metalayer.system import capture
from metalayer.utils import slugify, get_page_id


class CaptureProducer(Thread):

    def __init__(self, interval, buffer, **capture_kwargs):
        super().__init__()
        self.interval = interval
        self.buffer = buffer
        self.capture_kwargs = capture_kwargs
        self.reset_timer()
        # Platform-agnostic listeners
        self.mouse_listener = MouseListener(on_click=self.cancel_timer, on_scroll=self.cancel_timer)
        self.keyboard_listener = KeyboardListener(on_press=self.cancel_timer)

        self.running = False
        self.capture_threads = []

    def cancel_timer(self, *args):
        self.timer.cancel()

    def reset_timer(self):
        self.timer = Timer(self.interval, self.capture)

    def capture(self):
        capture_thread = CaptureThread(self.buffer, **self.capture_kwargs)
        self.capture_threads.append(capture_thread)
        capture_thread.start()
        capture_thread.join()
        self.capture_threads.remove(capture_thread)

    def start(self):
        print('Capture started')
        self.running = True
        self.mouse_listener.start()
        self.keyboard_listener.start()
        super().start()

    def join(self, timeout=None):
        super().join(timeout)
        self.keyboard_listener.join()
        self.mouse_listener.join()
        for t in self.capture_threads:
            t.join()
        self.running = False
        print('Capture finished, waiting on consumer to finish...')

    def run(self):
        while self.running:
            self.timer.start()
            # Timer either gets cancelled by mouse/keyboard event or finishes and calls capture
            self.timer.join()
            self.reset_timer()

    def stop(self):
        self.running = False
        self.timer.cancel()
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        for t in self.capture_threads:
            t.join()
        self.buffer.put(['stop'])


class CaptureThread(Thread):

    def __init__(self, buffer, save_sites=True):
        super().__init__()
        self.buffer = buffer
        self.save_sites = save_sites

    def run(self):
        try:
            dt = datetime.now()
            windows = capture.get_windows(self.save_sites)
            if len(windows) == 0:
                print('No windows found')
                return
            self.save_thumbnails(windows)
            self.buffer.put(('parse', dt, windows))

        except Exception as e:
            print('[ERROR] Capture Failed!')
            print(e)

    def save_thumbnails(self, windows):
        for i, window in enumerate(windows):
            app = window['app']
            title = window['title']
            page_id = get_page_id(app, title)
            window['page_id'] = page_id

            window_crop = window['screenshot']
            thumb_path = os.path.join(THUMBNAIL_DIR, page_id + ".png")
            if not os.path.exists(thumb_path):
                Image.fromarray(window_crop).save(thumb_path)


def capture_test():
    import time
    from multiprocessing import Queue

    def dummy_consumer(buffer):
        while True:
            action, *_ = buffer.get()
            if action == 'stop':
                break

    buffer = Queue()
    producer_thread = CaptureProducer(1, buffer, save_sites=False)
    consumer_thread = Thread(target=dummy_consumer, args=[buffer])

    consumer_thread.start()
    producer_thread.start()
    time.sleep(5)
    producer_thread.stop()
    producer_thread.join()
    consumer_thread.join()


if __name__ == '__main__':
    capture_test()
