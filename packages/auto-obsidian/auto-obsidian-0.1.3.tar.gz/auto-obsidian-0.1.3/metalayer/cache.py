import numpy as np

from collections import deque


# TODO:
# There's a bug where each image gets saved 2-3 times.
# Need to investigate this more, but for now I relaxed comparison to 99% similarity rather than 100%
class WindowCache():

    def __init__(self, window_cache_size=10, max_cache_size=100):
        self.cache = {}
        self.cache_order = []
        self.window_cache_size = window_cache_size
        self.max_cache_size = max_cache_size

    def __contains__(self, item):
        app_name, window_name, display_crop = item
        return self._check_cache(app_name, window_name, display_crop)

    def _check_cache(self, app_name, window_name, display_crop):
        dup = False
        k = (app_name, window_name)
        try:
            self.cache_order.remove(k)
        except ValueError:
            pass
        self.cache_order.append(k)

        if k not in self.cache:
            self.cache[k] = deque(maxlen=self.window_cache_size)

        for prev_crop in self.cache[k]:
            if prev_crop.shape != display_crop.shape:
                continue
            percent_diff = 100 * np.sum(np.not_equal(prev_crop, display_crop)) / prev_crop.size
            if percent_diff < 1:
                dup = True
                break

        if not dup:
            self.cache[k].append(display_crop)

        if sum(map(len, self.cache.values())) > self.max_cache_size:
            oldest = self.cache_order[0]
            self.cache[oldest].popleft()
            if len(self.cache[oldest]) == 0:
                del self.cache[oldest]
                self.cache_order.pop(0)

        return dup
