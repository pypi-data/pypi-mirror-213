from logging import LogRecord
from logging.handlers import BufferingHandler
from typing import Any, Callable

from buffering_queue_logger.send_logs_utils import C, K, send_logs_to_destination


class BufferingQueueHandler(BufferingHandler):
    """Build up a buffer of log records and send them to a destination when full."""

    def __init__(
        self,
        capacity: int,
        url: str,
        get_log_aggregator_key_func: Callable[[LogRecord, C | None], K],
        get_request_headers_func: Callable[[dict[str, Any], K], dict[str, Any]],
        chunk_size: int,
        context: C | None = None,
        ignore_runtime_errors_on_send: bool = True,
    ):
        super().__init__(capacity)
        self.url = url
        self.get_log_aggregator_key_func = get_log_aggregator_key_func
        self.get_request_headers_func = get_request_headers_func
        self.chunk_size = chunk_size
        self.context = context
        self.ignore_runtime_errors_on_send = ignore_runtime_errors_on_send

    def flush(self):
        """Send log records to a destination and empty the buffer."""
        if not len(self.buffer):
            return

        self.acquire()

        try:
            send_logs_to_destination(
                url=self.url,
                records=[x for x in self.buffer],
                format_func=self.format,
                get_log_aggregator_key_func=self.get_log_aggregator_key_func,
                get_request_headers_func=self.get_request_headers_func,
                chunk_size=self.chunk_size,
                context=self.context,
                ignore_runtime_errors_on_send=self.ignore_runtime_errors_on_send,
            )

            self.buffer.clear()
        finally:
            self.release()
