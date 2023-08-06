from logging import LogRecord
from logging.handlers import QueueHandler
from queue import Queue
from typing import Any, Callable

from buffering_queue_logger.handlers import BufferingQueueHandler
from buffering_queue_logger.listeners import BufferingQueueListener
from buffering_queue_logger.send_logs_utils import C, K


def get_buffering_queue_logger(
    capacity: int,
    url: str,
    get_log_aggregator_key_func: Callable[[LogRecord, C | None], K],
    get_request_headers_func: Callable[[dict[str, Any], K], dict[str, Any]],
    chunk_size: int,
    flush_buffer_every_x_secs: int,
    context: C | None = None,
    ignore_runtime_errors_on_send: bool = True,
    max_iterations: int | None = None,
    curr_time_ns_func: Callable[[], int] | None = None,
) -> tuple[QueueHandler, BufferingQueueListener]:  # pragma: no cover
    """Prepare queue, send / receive handlers, and thread for buffering queue logger.

    Thanks to:
    https://stackoverflow.com/questions/46754062
    /implementing-non-blocking-remote-logging-handler
    """
    # Logs pass from other threads to the logging thread via this queue
    log_queue: Queue = Queue(-1)

    # Other threads send logs to this handler, which sends them to the queue
    handler = QueueHandler(log_queue)

    # This handler receives logs from the queue and sends to the destination in batches
    receive_handler = BufferingQueueHandler(
        capacity=capacity,
        url=url,
        get_log_aggregator_key_func=get_log_aggregator_key_func,
        get_request_headers_func=get_request_headers_func,
        chunk_size=chunk_size,
        context=context,
        ignore_runtime_errors_on_send=ignore_runtime_errors_on_send,
    )

    # Prepare a thread that makes the buffering handler receive logs from the queue
    listener = BufferingQueueListener(
        buffering_log_queue=log_queue,
        buffering_handler=receive_handler,
        flush_buffer_every_x_secs=flush_buffer_every_x_secs,
        max_iterations=max_iterations,
        curr_time_ns_func=curr_time_ns_func,
    )

    # Calling code should call:
    #     listener.start()
    # and should call (for any logger whose logs should go to the buffering queue):
    #     logger.add(handler)
    return handler, listener
