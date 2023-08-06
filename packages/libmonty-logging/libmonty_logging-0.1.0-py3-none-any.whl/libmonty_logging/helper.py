#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
import logging.config
import os.path
from typing import Callable

# imports: dependencies
from xdg_base_dirs import xdg_state_home


def _state_dir_path(program_name: str) -> str:
    state_dir_path = os.path.join(xdg_state_home(), program_name)

    if not os.path.isdir(state_dir_path):
        os.makedirs(state_dir_path, mode=0o740, exist_ok=True)

    return state_dir_path


def _log_file_name(program_name: str, program_version: str) -> str:
    return f'{program_name}-{program_version}.log'


def log_file_path(program_name: str, program_version: str) -> str:
    state_dir_path: str = _state_dir_path(program_name)
    log_file_name: str = _log_file_name(program_name, program_version)
    return os.path.join(state_dir_path, log_file_name)

def apply_config(program_name: str, program_version: str, configurator: Callable) -> None:
    config = configurator(program_name, program_version)
    logging.config.dictConfig(config)
