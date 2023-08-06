from typing import Any, Dict, Optional, Union
from uuid import uuid4

import confluent_kafka as ck
import orjson

from . import get_logger


class Consumer:
    def __init__(
        self,
        host: str,
        port: Union[int, str],
        group_id: str,
    ) -> None:
        self.c = ck.Consumer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "group.id": group_id,
                "enable.auto.commit": False,
                "auto.offset.reset": "earliest",
            }
        )
        self.log = get_logger(__name__)
