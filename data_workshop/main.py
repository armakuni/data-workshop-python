import time

from data_workshop.actors.adding_actor import AddingActor, get_total

if __name__ == "__main__":
    adding_actor = AddingActor.start()
    adding_actor.tell(0.5)
    adding_actor.tell(0.1)
    adding_actor.tell(0.4)
    adding_actor.tell(10.0)

    while not adding_actor.actor_inbox.empty():
        time.sleep(0.1)

    print(f"Total: {adding_actor.ask(get_total)}")
    adding_actor.stop()
