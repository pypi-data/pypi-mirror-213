# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from typing import Optional


class OutputDirectories:
    def __init__(self, output_base_directory: Optional[pathlib.Path]):
        self._output_base_directory = output_base_directory

    def __call__(
        self, input_file: pathlib.Path, input_base_directory: Optional[pathlib.Path]
    ) -> pathlib.Path:
        output_directory: pathlib.Path
        if not self._output_base_directory:
            output_directory = input_file.parent
        elif not input_base_directory:
            output_directory = self._output_base_directory
        else:
            file_relative_to_directory = input_file.relative_to(input_base_directory)
            output_directory = self._output_base_directory / file_relative_to_directory.parent
        return output_directory
