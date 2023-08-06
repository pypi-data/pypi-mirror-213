# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for handling utility methods that are used across the
mlcvzoo_mmdetection package.
"""

import logging
from typing import Any, Dict, Optional, Tuple

from mmengine.config import Config

logger = logging.getLogger(__name__)


def init_mmdetection_config(
    config_path: str,
    cfg_options: Optional[Dict[str, Any]] = None,
) -> Config:
    # Build config provided by mmdetection framework
    logger.info("Load mmdetection config from: %s", config_path)

    cfg = Config.fromfile(config_path)
    if cfg_options is not None:
        cfg.merge_from_dict(cfg_options)

    return cfg


def modify_config(config_path: str, string_replacement_map: Dict[str, str]) -> str:
    with open(file=config_path, mode="r", encoding="'utf-8") as config_file:
        config_file_content = config_file.readlines()

    new_config_file_content = list()
    for config_content in config_file_content:
        new_config_content = config_content

        for replacement_key, replacement_value in string_replacement_map.items():
            if replacement_key in config_content:
                new_config_content = new_config_content.replace(
                    replacement_key, replacement_value
                )

                logger.info(
                    "Replace '%s' in config-line '%s' with '%s'",
                    replacement_key,
                    new_config_content,
                    replacement_value,
                )

        new_config_file_content.append(new_config_content)

    new_config_path = config_path.replace(".py", "_local.py")
    with open(file=new_config_path, mode="w+", encoding="'utf-8") as new_config_file:
        new_config_file.writelines(new_config_file_content)

    return new_config_path
