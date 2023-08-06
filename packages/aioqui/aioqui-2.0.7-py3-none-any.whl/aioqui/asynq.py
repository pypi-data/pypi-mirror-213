from qasync import QApplication, run as qrun, asyncSlot  # to import `asyncSlot` from `asynq`
from asyncio import exceptions, Future, AbstractEventLoop, get_event_loop
from typing import Callable, Awaitable
from functools import partial
import sys


def run(amain: Callable[[], Awaitable[None]]) -> None:
    async def wrap():
        def close_future(future: Future, loop: AbstractEventLoop) -> None:
            loop.call_later(10, future.cancel)
            future.cancel()

        future = Future()
        if hasattr(qapp := QApplication.instance(), 'aboutToQuit'):
            getattr(qapp, 'aboutToQuit').connect(partial(close_future, future, get_event_loop()))
        await amain()
        await future

    try:
        qrun(wrap())
    except exceptions.CancelledError:
        sys.exit(0)


# def to_async_slot(to_call):
#     @asyncSlot()
#     async def wrapped():
#         print(type(to_call))
#         if to_call.__class__.__name__ in ('function', 'method'):
#             await to_call()
#         # elif
#     return wrapped
