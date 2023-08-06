from turbo_queue import KafkaEnqueue

class Consumer:
    def __init__(self):
        print("calling __init__() newConsumer...")

    def start_enqueue_from_kafka(self, DL_HOST_ID, process_id, brokers):
        # logging.basicConfig(filename=f'from_kafka_for_chron_{DL_HOST_ID}_{KEEPER_INSTANCE}_{proc_num}.log',level=logging.INFO)
        enqueue_from_kafka = KafkaEnqueue()
        enqueue_from_kafka.turbo_queue_queue_name = "worker_ready"
        enqueue_from_kafka.turbo_queue_root_path = "/data/turbo-queues"
        enqueue_from_kafka.turbo_queue_max_ready_files = 8
        enqueue_from_kafka.turbo_queue_max_events_per_file = 10000
        enqueue_from_kafka.kafka_client_id = (
            f"""test01_intel_worker_{str(DL_HOST_ID)}_{str(process_id)}"""
        )
        enqueue_from_kafka.kafka_brokers = brokers
        enqueue_from_kafka.kafka_group_id = "test06_intel_worker"
        enqueue_from_kafka.kafka_auto_offset_reset = "earliest"
        enqueue_from_kafka.kafka_subscribe("ready")
        enqueue_from_kafka.start()


def start(**kwargs):
    get_events = Consumer()
    get_events.start_enqueue_from_kafka(kwargs["host_id"], kwargs["process_id"], kwargs["brokers"])
    print("consumer ready")
