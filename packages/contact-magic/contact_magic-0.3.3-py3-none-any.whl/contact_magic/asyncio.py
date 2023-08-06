import asyncio
from asyncio import QueueEmpty

from contact_magic.conf.settings import SETTINGS


async def do_bulk(ops: list, max_workers: int = SETTINGS.MAX_WORKERS):
    """
    Bulk operation
    This function can be used to run bulk operations
    using a limited number of concurrent requests.
    """
    results = [None for _ in range(len(ops))]

    queue = asyncio.Queue()

    for job in enumerate(ops):
        await queue.put(job)

    workers = [_worker(queue, results) for _ in range(max_workers)]

    await asyncio.gather(*workers)

    return results


async def _worker(queue: asyncio.Queue, results: list):
    while True:
        try:
            index, op = queue.get_nowait()
        except QueueEmpty:
            break

        try:
            response = await op[0](**op[1])
            results[index] = response
        except Exception as e:
            # log warning
            results[index] = {"data": {}, "index": 0}
        queue.task_done()
