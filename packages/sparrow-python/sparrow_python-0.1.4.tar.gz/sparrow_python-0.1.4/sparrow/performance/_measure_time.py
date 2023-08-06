import time
from rich.text import Text
from rich import print


class MeasureTime:
    def __init__(self, prec=2, logger=None, gpu=False):
        if gpu:
            import torch
            self.cuda_sync = torch.cuda.synchronize
        self._cost_time = 0.
        self._start_time = time.time()
        self._logger = logger
        self._msg = None
        self._prec: int = prec

    def start(self, gpu=False):
        if gpu:
            self.cuda_sync()
        self._start_time = time.time()
        return self

    def show_interval(self, msg=None, gpu=False):
        if gpu:
            self.cuda_sync()
        self._msg = msg
        self._cost_time = time.time() - self._start_time
        self._start_time = time.time()
        self._show()
        return self.get_cost()

    def get_cost(self):
        return f"{self._cost_time:.{int(self._prec)}E}"

    def _show(self):
        cost_time = self.get_cost()
        msg = f"{self._msg}\t" if self._msg else ''
        if self._logger:
            show_string = f"{msg}cost time: {cost_time}s"
            self._logger.debug(show_string)
        else:
            rgb_cost_time = Text(cost_time, style='green')
            rgb_msg = Text(f"{msg}", style="cyan")
            str_tuple = (rgb_msg, 'cost time: ', rgb_cost_time)
            print(*str_tuple, sep='')
