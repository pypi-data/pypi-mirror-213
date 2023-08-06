import os

import turbo_queue

import consumer
import worker
import producer

DL_HOST_ID = os.getenv("DL_HOST_ID")
BROKERS = "172.24.57.5:9092,172.24.57.6:9092,172.24.57.7:9092"


def cleanup():
    clean_worker_ready = turbo_queue.Startup()
    clean_worker_ready.queue_name = "worker_ready"
    clean_worker_ready.root_path = "/data/turbo-queues"
    clean_worker_ready.on_start_cleanup()

    clean_intel_ready = turbo_queue.Startup()
    clean_intel_ready.queue_name = "intel_ready"
    clean_intel_ready.root_path = "/data/turbo-queues"
    clean_intel_ready.on_start_cleanup()
    return True


cleanup()

# create the app
app = turbo_queue.MultiTask()

# create the kafka consumer
consumer_task = turbo_queue.TaskGroup()
consumer_task.function_to_call = consumer.start
consumer_task.process_count = 8
consumer_task.process_number_start = 11
consumer_task.kwargs = {
    "host_id": DL_HOST_ID,
    "brokers": BROKERS,
    "task_name": "intel_consumer",
}
# add the task to the list of processes to run
app.add_task(consumer_task)

# create the task to process the events
work_task = turbo_queue.TaskGroup()
work_task.function_to_call = worker.start
work_task.process_count = 8
work_task.process_number_start = 11
work_task.kwargs = {
    "host_id": DL_HOST_ID,
    "brokers": BROKERS,
    "task_name": "worker",
}
# add the task to the list of processes to run
app.add_task(work_task)

# create the kafka producer
producer_task = turbo_queue.TaskGroup()
producer_task.function_to_call = producer.start
producer_task.process_count = 12
producer_task.process_number_start = 11
producer_task.kwargs = {
    "host_id": DL_HOST_ID,
    "brokers": BROKERS,
    "task_name": "intel_producer",
}
## add the task to the list of processes to run
app.add_task(producer_task)

# start the app
app.start_all()
