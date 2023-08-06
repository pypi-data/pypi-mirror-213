from dataclasses import field
from typing import List

from pydantic.dataclasses import dataclass

from qwak_sdk.commands.audience._logic.config.v1.audience_config import AudienceConfig


@dataclass
class Spec:
    audiences: List[AudienceConfig] = field(default_factory=list)
