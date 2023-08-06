from pathlib import Path
from typing import Optional, Union

import yaml

from qwak_sdk.commands.auto_scalling._logic.config import Config


def parse_autoscaling_from_yaml(file_path: Optional[Union[Path, str]] = None) -> Config:
    if file_path:
        file_obj = Path(file_path)
        if file_obj.exists():
            autoscaling_dict = yaml.safe_load(file_obj.open("r"))
            autoscaling_config = Config
            return autoscaling_config(**autoscaling_dict)
        else:
            raise FileNotFoundError(
                f"autoscaling file {file_obj} definition isn't found"
            )
    else:
        return Config()
