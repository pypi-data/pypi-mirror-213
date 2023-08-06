#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: project
from libmonty_logging import helper


def config(program_name: str, program_version: str) -> dict:
    log_file_path: str = helper.log_file_path(program_name, program_version)

    return {
        'version': 1,
        'formatters': {
            'form01': {
                'format': '[%(asctime)s] [%(levelname)-8s] %(message)s',
                'datefmt': '%H:%M:%S'
            },
            'form02': {
                'format': '[%(asctime)s] [%(levelname)-8s] %(message)s'
            }
        },
        'handlers': {
            'hand01': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'form01',
                'stream': 'ext://sys.stdout'
            },
            'hand02': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'form02',
                'filename': log_file_path,
                'mode': 'w',
                'encoding': 'UTF-8'
            }
        },
        'loggers': {
            'root': {
                'level': 'NOTSET',
                'handlers': ['hand01', 'hand02']
            }
        }
    }
