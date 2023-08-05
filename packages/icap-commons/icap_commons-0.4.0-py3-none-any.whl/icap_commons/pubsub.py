from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound
from loguru import logger
from typing import Any, Optional, Dict, Callable


class PubSubPublish:
    def __init__(self, project_id: str, topic_name: str):
        self.project_id = project_id
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
                    project_id=project_id,
                    topic=topic_name
                )
        self.publisher = pubsub_v1.PublisherClient()
        self.__setup_publisher()

    def __setup_publisher(self) -> Any:
        logger.debug(f"Setting up the {self.topic_name} pubsub")
        publisher = pubsub_v1.PublisherClient()
        try:
            publisher.get_topic(topic=self.topic_name)
            return publisher
        except NotFound:
            logger.error(f"Pubsub not found {self.topic_name}, please make sure\
            that the name of the pubsub topic is correct and a pubsub with same \
            topic exists in the gcp project")
            raise Exception(f"Pubsub {self.topic_name} not found")
        except Exception as e:
            raise Exception(
                f"Error getting {self.topic_name} pubsub: {e}")

    def publish_messsage(
            self,
            data: str,
            attr: Optional[Dict[str, Any]] = None) -> Any:
        logger.info(f"publishing message to {self.topic_name}: {data}")
        if attr:
            future = self.publisher.publish(
                    self.topic_name,
                    data.encode("utf-8"),
                    **attr)
        else:
            future = self.publisher.publish(
                    self.topic_name,
                    data.encode("utf-8"))
        return future.result()


class PubSubSubscribe:

    def __init__(
            self,
            project_id: str,
            topic_name: str,
            subscription_name: str,
            callback: Callable) -> None:
        self.project_id = project_id
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
                project_id=project_id,
                topic=topic_name
                )
        self.subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
                project_id=project_id,
                sub=subscription_name
                )
        self.callback = callback
        self.subscriber = self.__subscribe()

    def __subscribe(self) -> Any:
        logger.debug("Setting up the subscriber")
        with pubsub_v1.SubscriberClient() as subscriber:
            try:
                subscriber.create_subscription(
                        name=self.subscription_name,
                        topic=self.topic_name)

                subscriber.subscribe(self.subscription_name, self.callback)
                return subscriber
            except Exception as e:
                logger.error(f"Error setting up subscriber {e}")
            finally:
                return subscriber


class PubSub:
    publisher: Optional[PubSubPublish] = None


# list all the pubsubs that needs the setup
notification_pubsub = PubSub()


def setup_pubsub_publisher(
        project_id: str, topic_name: str, pubsub: PubSub) -> None:
    pubsub.publisher = PubSubPublish(project_id, topic_name)


# Use this for pull, this is not useful in case of cloudrun
# for this the application should always be running
"""
def setup_pubsub_subscriber(
        project_id: str,
        topic_name: str,
        subscription_name: str,
        callback: Callable) -> None:
    pubsub.subscriber = PubSubSubscribe(
            project_id,
            topic_name,
            subscription_name,
            callback)
"""
