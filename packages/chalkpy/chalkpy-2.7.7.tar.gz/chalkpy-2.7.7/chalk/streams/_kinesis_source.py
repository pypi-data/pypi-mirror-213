from typing import Any, List, Optional, Union

from pydantic import BaseModel

from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration


class KinesisSource(StreamSource, BaseModel, frozen=True):
    stream_name: Optional[Union[str, List[str]]] = None
    """The ARN of your stream"""

    stream_arn: Optional[Union[str, List[str]]] = None
    """The ARN of your stream"""

    topic: Optional[str] = None
    """The name of the topic to subscribe to."""

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_topic: Optional[str] = None
    """
    Kinesis topic to send messages when message processing fails
    """

    def __init__(
        self,
        *,
        stream_name: Optional[str] = None,
        stream_arn: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_topic: Optional[str] = None,
        name: Optional[str] = None,
    ):
        super(KinesisSource, self).__init__(
            stream_name=stream_name,
            stream_arn=stream_arn,
            name=name,
            late_arrival_deadline=late_arrival_deadline,
            dead_letter_queue_topic=dead_letter_queue_topic,
        )

    def _config_to_json(self) -> Any:
        return self.json()
