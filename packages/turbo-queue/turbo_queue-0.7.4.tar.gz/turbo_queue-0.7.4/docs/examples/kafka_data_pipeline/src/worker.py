import asyncio
import json
import logging

import turbo_queue


class Work:
    def __init__(self):
        print("calling __init__() worker...")
        self.count_process_doc = 0
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def start_loop(self):
        self.loop.run_forever()

    def start_enqueue_from_worker(self):
        self.enqueue_from_worker = turbo_queue.Enqueue()
        self.enqueue_from_worker.setup_logging()
        self.enqueue_from_worker.queue_name = "intel_ready"
        self.enqueue_from_worker.root_path = "/data/turbo-queues"
        self.enqueue_from_worker.max_ready_files = 8
        self.enqueue_from_worker.max_events_per_file = 10000
        self.enqueue_from_worker.start()
        self.loop.create_task(self.loadEvents())
        return

    def start_dequeue_to_worker(self):
        self.dequeue_to_worker = turbo_queue.Dequeue()
        self.dequeue_to_worker.queue_name = "worker_ready"
        self.dequeue_to_worker.root_path = "/data/turbo-queues"

    async def loadEvents(self):
        self.enqueue_from_worker.update_enqueue_active_state()
        while self.enqueue_from_worker.enqueue_active:
            get_data = self.dequeue_to_worker.get()
            doc = next(get_data)
            while doc:
                ## call function to process this doc
                doc = await self.process_doc(doc)
                # send on to the next queue
                self.enqueue_from_worker.add(doc)
                # get the next doc from the inbound queue:
                doc = next(get_data)
        await asyncio.sleep(0.05)
        self.loop.create_task(self.loadEvents())

    async def process_doc(self, doc):
        """process a document from the queue

        Args:
            doc (dict): a dictionary, representing the json document that was removed from the queue

        Returns:
            doc: a new or modified json documet to send downstream
        """

        self.count_process_doc += 1
        return doc


def start(**kwargs):
    start_worker = Work()
    start_worker.start_enqueue_from_worker()
    start_worker.start_dequeue_to_worker()
    start_worker.start_loop()
    print("worker ready")
