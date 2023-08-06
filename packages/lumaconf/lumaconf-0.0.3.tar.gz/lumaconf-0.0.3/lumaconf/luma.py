import json
from . import ConfigFactory, ConfigTree
from .converter import HOCONConverter
import os
from typing import Dict, List, Any, Union


def convert_bools(val: Any):
    """Recursively convert booleans in a dict/list"""
    if isinstance(val, dict):
        return {k: convert_bools(val[k]) for k in val}
    elif isinstance(val, list):
        return [convert_bools(x) for x in val]
    elif isinstance(val, str):
        val_strip = val.strip()
        # When bools come in on the command line they are in string format.
        # This is an easy point which we can iterate over everything.
        if val_strip == "True" or val_strip == "true":
            return True
        elif val_strip == "False" or val_strip == "false":
            return False
    return val


def merge_dicts(
    a: Dict, b: Dict, convert_bools: bool = False, overwrite_existing: bool = True
):
    """Recursively merge dict b into a"""
    for k in b.keys():
        if k in a and isinstance(a[k], dict) and isinstance(b[k], dict):
            merge_dicts(
                a[k],
                b[k],
                convert_bools=convert_bools,
                overwrite_existing=overwrite_existing,
            )
        else:
            # When bools come in on the command line they are in string format.
            # This is an easy point which we can iterate over everything.
            if convert_bools and isinstance(b[k], str):
                if b[k] == "True" or b[k] == "true":
                    b[k] = True
                elif b[k] == "False" or b[k] == "false":
                    b[k] = False

            if not overwrite_existing and k in a:
                continue
            a[k] = b[k]


def get_config_path(
    root: Dict, key_path: str, tree_path: List[str] = [], require: bool = True
):
    """
    Get item in config tree, where key_path is something
    like 'a.b.c'
    """
    node = root
    for key_item in key_path.split("."):
        if isinstance(node, dict):
            node = node.get(key_item, None)
        elif isinstance(node, list):
            node = node[int(key_item)]
        else:
            node = None
            break
    if node is None and require:
        raise RuntimeError(
            f"config path '{key_path}' "
            + f"does not exist (at '{'.'.join(tree_path)}')"
        )
    return node



def load(
    config: Union[str, ConfigTree] = "base.conf",
    override: Union[None, str, Dict[str, Any]] = None,
) -> ConfigTree:
    """
    Load HOCON/json config file.
    If config is a ConfigTree it will pass through directly.
    """
    # If we are to override the config then we load it here and pass it in as a string.
    if isinstance(config, str):
        if not os.path.isfile(config):
            config = os.path.join("configs", config)
        use_override = False
        if override is not None:
            # For config override, we will continue to use JSON since it can be
            # passed from the infra
            if isinstance(override, str):
                if override.strip() == "":
                    override = {}
                else:
                    override = json.loads(override)
            override = convert_bools(override)

            if override:
                override = ConfigFactory.from_dict(override)
                # Convert true/false
                override_hocon = HOCONConverter.to_hocon(override)
                print("Override config:\n", override_hocon)
                config_dir = os.path.dirname(config)
                config_name = os.path.basename(config)
                override_hocon = f'include "{config_name}"\n' + override_hocon

                # Parse HOCON from override
                config_data: ConfigTree = ConfigFactory.parse_string(
                    override_hocon, basedir=config_dir
                )
                use_override = True
            else:
                # pyhocon to_hocon is weirdly bugged and gives an invalid result
                pass

        if not use_override:
            # Parse HOCON directly
            config_data: ConfigTree = ConfigFactory.parse_file(config)
    else:
        config_data = config
    return config_data
