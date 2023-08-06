from typing import Any, Tuple, Union

from qwak.inner.tool.run_config import QwakConfigBase, YamlConfigMixin


def config_handler(
    config: Union[QwakConfigBase, YamlConfigMixin, Any],
    from_file: str,
    out_conf: bool,
    sections: Tuple[str, ...] = (),
    **kwargs,
) -> Any:
    conf: Union[QwakConfigBase, YamlConfigMixin] = config.from_yaml(from_file)
    conf.merge_cli_argument(sections=sections, **kwargs)
    if out_conf:
        print(conf.to_yaml())

    return conf
