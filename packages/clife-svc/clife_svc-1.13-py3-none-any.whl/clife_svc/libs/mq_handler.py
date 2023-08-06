from clife_svc.libs.log import klogger, clogger


class MQHandler:

    def __init__(self, app):
        self._app = app
        self._producer = None
        self._producer_topic = None
        self._consumer = None
        self._consumer_group = None
        self._consumer_sub_topics = []
        try:
            from rocketmq.client import Producer, PushConsumer, Message
        except NotImplementedError:
            clogger.warning(f'rocketMQ does not support Windows, Message Queue disabled.')
        else:
            try:
                self._rocket_url = app.get_conf('rocket.mq.url')
                if self._rocket_url:
                    clogger.info(f'rocketMQ URL: {self._rocket_url}')
                    self._producer_topic = app.get_conf('rocket.mq.producer.topic')
                    if not self._producer_topic:
                        clogger.warning(f'rocketMQ Producer: Default topic not found. Topic required when send message.')
                    # 创建消费者
                    self._consumer_group = app.get_conf('rocket.mq.consumer.group')
                    if not self._consumer_group:
                        clogger.warning(f'rocketMQ Consumer: consumer group not found, consumer disabled.')
                    else:
                        self._consumer = PushConsumer(self._consumer_group)
                        self._consumer.set_namesrv_addr(self._rocket_url)
                else:
                    clogger.warning(f'rocketMQ URL not found, Message Queue disabled.')
            except Exception as e:
                clogger.warning(f'Error connect rocketMQ, Message Queue disabled.error_info:{e}')

    def add_subscribe(self, call_back, topic=None):
        if self._consumer:
            if not callable(call_back):
                raise Exception('Call back function must be callable')
            topic = topic if topic else self._app.get_conf('rocket.mq.consumer.topic')
            if not topic:
                raise Exception('Topic is required for rocketMQ Consumer')
            elif topic and topic in self._consumer_sub_topics:
                raise Exception(f'Consumer can not subscribe {topic} again')
            else:
                self._consumer_sub_topics.append(topic)
                self._consumer.subscribe(topic, call_back)
        else:
            raise Exception('rocketMQ consumer disabled')

    def start_consumer(self):
        if len(self._consumer_sub_topics) > 0:
            self._consumer.start()

    def send_sync(self, body, topic=None, keys=None, tags=None):
        if not self._producer:
            from rocketmq.client import Producer
            if self._rocket_url:
                self._producer = Producer(self._app.app_name)
                self._producer.set_namesrv_addr(self._rocket_url)
                self._producer.start()
            else:
                raise Exception('rocketMQ URL not found, Message Queue disabled.')

        topic = topic if topic else self._producer_topic
        if topic:
            from rocketmq.client import Message
            msg = Message(topic)
            msg.set_body(body)
            if keys:
                msg.set_keys(keys)
            if tags:
                msg.set_tags(tags)
            self._producer.send_sync(msg)
            klogger.info('rocketMQ message sent successfully')
        else:
            raise Exception('Topic is required for rocketMQ producer')