#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
import logging


def program_header(program_name: str,
                   program_version: str = None,
                   underliner: str = '-'
                   ) -> None:

    if len(underliner) != 1:
        raise ValueError(f'Argument "underliner" must be 1 character long: "{underliner}"')

    header = f'{program_name}'
    
    if program_version is not None:
        header += f'{program_version}'

    logging.info(header)
    logging.info('-' * len(header))
