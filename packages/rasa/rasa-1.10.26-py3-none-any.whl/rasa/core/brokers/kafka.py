import json
import logging
import time
from asyncio import AbstractEventLoop
from typing import Optional

from rasa.constants import DOCS_URL_EVENT_BROKERS
from rasa.core.brokers.broker import EventBroker
from rasa.utils.common import raise_warning
from rasa.utils.io import DEFAULT_ENCODING
from rasa.exceptions import RasaException

logger = logging.getLogger(__name__)


class KafkaProducerInitializationError(RasaException):
    """Raised if the Kafka Producer cannot be properly initialized."""


class KafkaEventBroker(EventBroker):
    def __init__(
        self,
        host,
        sasl_username=None,
        sasl_password=None,
        sasl_mechanism="PLAIN",
        ssl_cafile=None,
        ssl_certfile=None,
        ssl_keyfile=None,
        ssl_check_hostname=False,
        topic="rasa_core_events",
        client_id=None,
        partition_by_sender=False,
        security_protocol="SASL_PLAINTEXT",
        loglevel=logging.ERROR,
        group_id=None,
    ) -> None:

        self.producer = None
        self.host = host
        self.topic = topic
        self.client_id = client_id
        self.partition_by_sender = partition_by_sender
        self.security_protocol = security_protocol
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.sasl_mechanism = sasl_mechanism
        self.ssl_cafile = ssl_cafile
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.ssl_check_hostname = ssl_check_hostname

        if group_id is not None:
            raise_warning(
                "The endpoint config includes the  `group_id` parameter for the `KafkaEventBroker`, \
                            which is only used by Kafka consumers, not Kafka producers."
            )

        logging.getLogger("kafka").setLevel(loglevel)

    @classmethod
    async def from_endpoint_config(
        cls, broker_config, event_loop: Optional[AbstractEventLoop] = None,
    ) -> Optional["KafkaEventBroker"]:
        if broker_config is None:
            return None

        return cls(broker_config.url, **broker_config.kwargs)

    def publish(self, event, retries=60, retry_delay_in_seconds=5) -> None:
        if self.producer is None:
            self._create_producer()
            connected = self.producer.bootstrap_connected()
            if connected:
                logger.debug("Connection to kafka successful.")
            else:
                logger.debug("Failed to connect kafka.")
                return
        while retries:
            try:
                self._publish(event)
                return
            except Exception as e:
                logger.error(
                    f"Could not publish message to kafka host '{self.host}'. "
                    f"Failed with error: {e}"
                )
                connected = self.producer.bootstrap_connected()
                if not connected:
                    self._close()
                    logger.debug("Connection to kafka lost, reconnecting...")
                    self._create_producer()
                    connected = self.producer.bootstrap_connected()
                    if connected:
                        logger.debug("Reconnection to kafka successful")
                        self._publish(event)
                retries -= 1
                time.sleep(retry_delay_in_seconds)

        logger.error("Failed to publish Kafka event.")

    def _create_producer(self) -> None:
        import kafka

        hosts = [self.host]
        if type(self.host) == list:
            hosts = self.host

        if self.security_protocol == "SASL_PLAINTEXT":
            authentication_params = dict(
                sasl_plain_username=self.sasl_username,
                sasl_plain_password=self.sasl_password,
                sasl_mechanism=self.sasl_mechanism,
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "PLAINTEXT":
            authentication_params = dict(
                security_protocol=self.security_protocol, ssl_check_hostname=False,
            )
        elif self.security_protocol == "SSL":
            authentication_params = dict(
                ssl_cafile=self.ssl_cafile,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile,
                ssl_check_hostname=False,
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "SASL_SSL":
            authentication_params = dict(
                sasl_plain_username=self.sasl_username,
                sasl_plain_password=self.sasl_password,
                sasl_mechanism=self.sasl_mechanism,
                ssl_cafile=self.ssl_cafile,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile,
                ssl_check_hostname=self.ssl_check_hostname,
                security_protocol=self.security_protocol,
            )
        else:
            logger.error("Kafka security_protocol invalid or not set")
        try:
            self.producer = kafka.KafkaProducer(
                client_id=self.client_id,
                bootstrap_servers=hosts,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                **authentication_params,
            )
        except AssertionError as e:
            raise KafkaProducerInitializationError(
                f"Cannot initialise `KafkaEventBroker`: {e}"
            )

    def _publish(self, event) -> None:
        if self.partition_by_sender:
            partition_key = bytes(event.get("sender_id"), encoding=DEFAULT_ENCODING)
        else:
            partition_key = None

        logger.debug(
            f"Calling kafka send({self.topic}, value={event}, key={partition_key!s})"
        )
        self.producer.send(self.topic, value=event, key=partition_key)

    def _close(self) -> None:
        self.producer.close()


class KafkaProducer(KafkaEventBroker):
    def __init__(
        self,
        host,
        sasl_username=None,
        sasl_password=None,
        sasl_mechanism="PLAIN",
        ssl_cafile=None,
        ssl_certfile=None,
        ssl_keyfile=None,
        ssl_check_hostname=False,
        topic="rasa_core_events",
        security_protocol="SASL_PLAINTEXT",
        loglevel=logging.ERROR,
        group_id=None,
    ) -> None:
        raise_warning(
            "The `KafkaProducer` class is deprecated, please inherit "
            "from `KafkaEventBroker` instead. `KafkaProducer` will be "
            "removed in future Rasa versions.",
            FutureWarning,
            docs=DOCS_URL_EVENT_BROKERS,
        )

        super(KafkaProducer, self).__init__(
            host,
            sasl_username,
            sasl_password,
            sasl_mechanism,
            ssl_cafile,
            ssl_certfile,
            ssl_keyfile,
            ssl_check_hostname,
            topic,
            security_protocol,
            loglevel,
            group_id,
        )
