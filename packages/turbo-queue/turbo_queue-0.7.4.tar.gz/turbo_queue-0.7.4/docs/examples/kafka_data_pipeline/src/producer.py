from turbo_queue import KafkaDequeue

class Producer:
    def __init__(self):
        print("calling __init__() Producer...")

    def start_dequeue_to_kafka(self, DL_HOST_ID, process_id, brokers):
        # logging.basicConfig(filename=f'from_kafka_for_chron_{DL_HOST_ID}_{KEEPER_INSTANCE}_{proc_num}.log',level=logging.INFO)
        dequeue_to_kafka = KafkaDequeue()
        dequeue_to_kafka.turbo_queue_queue_name = "intel_ready"
        dequeue_to_kafka.turbo_queue_root_path = "/data/turbo-queues"
        #
        dequeue_to_kafka.kafka_client_id = (
            f"""test01_intel_worker_{str(DL_HOST_ID)}_{str(process_id)}"""
        )
        dequeue_to_kafka.kafka_brokers = brokers
        dequeue_to_kafka.kafka_producer_topic = "test0001"
        dequeue_to_kafka.start()


def start(**kwargs):
    get_events = Producer()
    get_events.start_dequeue_to_kafka(kwargs["host_id"], kwargs["process_id"], kwargs["brokers"])
    print("Producer ready")
