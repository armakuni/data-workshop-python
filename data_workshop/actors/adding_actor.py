from queue import Queue


class AddingActor:
    def __init__(self, inbox: "Queue[int|str]", actor_ref: Queue[int]) -> None:
        self.inbox = inbox
        self.actor_ref = actor_ref

    async def start(self) -> None:
        while True:
            message = self.inbox.get()
            if message == "stop":
                self.inbox.task_done()
                return

            print("Hello, world!")
            self.inbox.task_done()
