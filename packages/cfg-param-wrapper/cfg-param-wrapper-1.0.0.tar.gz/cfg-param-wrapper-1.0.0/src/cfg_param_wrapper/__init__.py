"""A Config parser library meant for easy plug and play."""
from .argparse_config import ArgparseConfig
from .cfg_dict import CfgDict
from .function_config_wrapper import wrap_config

ConfigArgParser = ArgparseConfig  # for compat
__all__: list[str] = ["ConfigArgParser", "ArgparseConfig", "CfgDict", "wrap_config"]
