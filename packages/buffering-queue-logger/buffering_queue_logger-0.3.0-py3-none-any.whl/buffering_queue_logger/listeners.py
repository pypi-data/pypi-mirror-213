from logging import LogRecord
from logging.handlers import QueueListener
from queue import Empty, Queue
from time import monotonic_ns, sleep
from typing import Any, Callable

from buffering_queue_logger.handlers import BufferingQueueHandler


def _monitor_queue_and_flush_buffer(
    buffering_log_queue: Queue,
    dequeue_func: Callable[[bool], LogRecord],
    sentinel_value: Any,
    handle_func: Callable[[LogRecord], None],
    buffering_handler: BufferingQueueHandler,
    flush_buffer_every_x_secs: int,
    max_iterations: int | None = None,
    curr_time_ns_func: Callable[[], int] | None = None,
):
    """Send logs from queue to receiving handler, and periodically flush the buffer."""
    has_task_done = hasattr(buffering_log_queue, "task_done")
    buffering_handler.flush()
    _curr_time_ns_func = (
        curr_time_ns_func if curr_time_ns_func is not None else monotonic_ns
    )
    prev_time_ns: int | None = None
    i = 0
    is_queue_exhausted = False

    while (not is_queue_exhausted) and (max_iterations is None or i < max_iterations):
        curr_time_ns = _curr_time_ns_func()

        try:
            # The Python core QueueListener passes block=True, which makes this loop
            # wait at this line, for as long as necessary, between log messages being
            # received. We instead pass block=False, because we want to keep looping
            # constantly, regardless of whether log messages are being received or not,
            # so that we can periodically flush the buffer.
            record = dequeue_func(False)

            if record is sentinel_value:  # pragma: no cover
                is_queue_exhausted = True

            if not is_queue_exhausted:
                handle_func(record)

            if has_task_done:
                buffering_log_queue.task_done()
        except Empty:  # pragma: no cover
            # The Python core QueueListener breaks out of the loop here. We instead
            # sleep for a wee bit, then let the buffer flush if it's time to do so,
            # then loop back around and check for more log messages.
            sleep(0.01)

        if (
            prev_time_ns is not None
            and (curr_time_ns - prev_time_ns) / 1_000_000_000
            >= flush_buffer_every_x_secs
        ):
            buffering_handler.flush()
            prev_time_ns = curr_time_ns

        if prev_time_ns is None:
            prev_time_ns = curr_time_ns

        if max_iterations is not None:
            i += 1


class BufferingQueueListener(QueueListener):  # pragma: no cover
    """Listen for logs in the queue and periodically flush the buffer."""

    def __init__(
        self,
        buffering_log_queue: Queue,
        buffering_handler: BufferingQueueHandler,
        flush_buffer_every_x_secs: int,
        respect_handler_level: bool = False,
        max_iterations: int | None = None,
        curr_time_ns_func: Callable[[], int] | None = None,
    ):
        self.buffering_handler = buffering_handler
        self.flush_buffer_every_x_secs = flush_buffer_every_x_secs
        self.max_iterations = max_iterations
        self.curr_time_ns_func = curr_time_ns_func

        super().__init__(
            buffering_log_queue,
            *[buffering_handler],
            respect_handler_level=respect_handler_level,
        )

    def _monitor(self):
        """Send logs from queue to receiving handler, and periodically flush the buffer.

        Overridden version of Python core's logging.handlers.QueueListener._monitor.
        """
        _monitor_queue_and_flush_buffer(
            buffering_log_queue=self.queue,
            dequeue_func=self.dequeue,
            sentinel_value=self._sentinel,
            handle_func=self.handle,
            buffering_handler=self.buffering_handler,
            flush_buffer_every_x_secs=self.flush_buffer_every_x_secs,
            max_iterations=self.max_iterations,
            curr_time_ns_func=self.curr_time_ns_func,
        )
