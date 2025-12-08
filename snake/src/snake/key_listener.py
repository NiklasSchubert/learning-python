from curses import window, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from threading import Thread
import time
from queue import Queue
from typing import Optional


class KeyListener:
    def __init__(self, max_size: int = 2) -> None:
        self.queue: Queue[int] = Queue(max_size)
        self._running: bool = False
        self._thread: Optional[Thread] = None
        self.KEYS = (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT)

    def _push(self, key: int) -> None:
        if self.queue.full():
            self.queue.get_nowait()  # drop oldest
        self.queue.put_nowait(key)

    def _reader(self, stdscr: window) -> None:
        stdscr.nodelay(True)
        self._running = True

        while self._running:
            key = stdscr.getch()
            if key != -1 and key in self.KEYS and key not in self.queue.queue:
                self._push(key)

            time.sleep(0.01)  # avoid burning CPU

    def start(self, stdscr: window) -> None:
        if self._thread is not None:
            return  # already running

        self._thread = Thread(
            target=self._reader,
            args=(stdscr,),
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._running = False
