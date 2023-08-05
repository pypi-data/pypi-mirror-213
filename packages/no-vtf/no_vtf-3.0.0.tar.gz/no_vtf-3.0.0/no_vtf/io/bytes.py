# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from no_vtf.io.io import IO


class BytesIO(IO[bytes]):
    def write(self, path: pathlib.Path, data: bytes) -> None:
        with open(path, "wb") as file:
            file.write(data)

    def readback(self, path: pathlib.Path, data: bytes) -> None:
        with open(path, "rb") as file:
            read_data = file.read()
            if data != read_data:
                raise RuntimeError(f"{path!r}: Data differs from what is in the file")
