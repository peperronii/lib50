import enum
import yaml
from . import errors
from . import _

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

class InvalidTag:
    def __init__(self, loader, prefix, node):
        self.tag = node.tag

class FileStatus(enum.Enum):
    Excluded = "!exclude"
    Included = "!include"
    Required = "!require"

class File:
    def __init__(self, loader, node):
        self.status = FileStatus(node.tag)
        self.name = node.value

class ConfigLoader(SafeLoader):
    pass
for member in FileStatus.__members__.values():
    ConfigLoader.add_constructor(member.value, File)
ConfigLoader.add_multi_constructor("", InvalidTag)

def load(content, tool, loader=ConfigLoader):
    """
    Parses content (contents of .cs50.yaml) with push50.config.ConfigLoader
    Raises InvalidConfigError
    """
    try:
        config = yaml.load(content, Loader=loader)
    except yaml.YAMLError:
        raise errors.InvalidConfigError(_("Config is not valid yaml."))

    try:
        config = config[tool]
    except (TypeError, KeyError):
        config = None

    try:
        files = config["files"]
    except (TypeError, KeyError):
        pass
    else:
        if not isinstance(files, list):
            raise errors.InvalidConfigError(_("files: entry in config must be a list"))

        for file in files:
            if not isinstance(file, File):
                raise errors.InvalidConfigError(
                    _("All entries in files: must be tagged with either !include, !exclude or !require"))

    _validate_config(config, tool)

    return config

def _validate_config(config, tool):
    if isinstance(config, dict):
        for item in config:
            _validate_config(config[item], tool)

    elif isinstance(config, list):
        for item in config:
            _validate_config(item, tool)

    elif isinstance(config, InvalidTag):
        raise errors.InvalidConfigError("{} is not a valid tag for {}".format(config.tag, tool))
