from agora_config import config
from agora_logging import logger
from .message_queue import MessageQueue, IoDataReportMsg


class BaseMqttClient():
    def __init__(self):
        self.messages = MessageQueue()
        self.server = "127.0.0.1"
        self.port = 707
        self.username = None
        self.password = None
        self.topics = set()

    def is_connected(self):
        return True

    def disconnect(self):
        pass

    def connect(self, limit: int):
        pass

    def update_topics(self, topics):
        self.topics = topics

    def send_message(self, topic, payload):
        if topic == "DataOut":
            self.messages.store_to_queue("DataIn", payload.encode("utf-8"))
        elif topic == "RequestOut":
            self.messages.store_to_queue("RequestIn", payload.encode("utf-8"))
        else:
            self.messages.store_to_queue(topic, payload.encode("utf-8"))

    def configure(self):
        self.server = config["AEA2:BusClient:Server"]
        if self.server == "":
            self.server = "127.0.0.1"

        self.port = config["AEA2:BusClient:Port"]
        if self.port == "":
            self.port = "707"

        topics = set()

        use_data_in = bool(config["AEA2:BusClient:UseDataIn"])
        if use_data_in:
            logger.warn(
                "Setting 'AEA2:BusClient:UseDataIn' has been deprecated.  Add 'DataIn' directly within 'AEA2:BusClient:Subscriptions' array instead.")
            topics.add("DataIn")

        use_request_in = bool(config["AEA2:BusClient:UseRequests"])
        if use_request_in:
            logger.warn(
                "Setting 'AEA2:BusClient:UseRequests' has been deprecated.  Add 'RequestIn' directly within 'AEA2:BusClient:Subscriptions' array instead.")
            topics.add("RequestIn")

        str_device_id = config["AEA2:BusClient:DeviceId"]
        try:
            IoDataReportMsg.default_device_id = int(str_device_id)
        except:
            IoDataReportMsg.default_device_id = 999

        subscriptions = config["AEA2:BusClient:Subscriptions"]
        if subscriptions != "":
            topics = topics.union(set(subscriptions))

        self.username = config["AEA2:BusClient:Username"]
        self.password = config["AEA2:BusClient:Password"]

        self.update_topics(topics)

    def log_config(self):
        logger.info("AEA2:BusClient:")
        logger.info(f"--- Server: {self.server}")
        logger.info(f"--- Port: {self.port}")
        logger.info(f"--- DeviceId: {IoDataReportMsg.default_device_id}")
        if len(self.topics) > 0:
            logger.info("--- Subscriptions:")
            for sub in self.topics:
                logger.info(f"   --- {sub}")
        else:
            logger.info("--- Subscriptions: <None>")
