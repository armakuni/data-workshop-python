import asyncio
from queue import Queue

import pytest

from data_workshop.actors.adding_actor import AddingActor


@pytest.mark.asyncio
async def test_fetch_number() -> None:
    inbox: "Queue[int|str]" = Queue()
    actor_ref: "Queue[int]" = Queue()
    actor = AddingActor(inbox, actor_ref)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(actor.start())
        inbox.put_nowait(123)
        inbox.put_nowait(333)
        inbox.put_nowait("stop")

    # assert actor_ref.get() == 123
    # actor_ref.task_done()
    # assert actor_ref.get() == 456
    # actor_ref.task_done()
