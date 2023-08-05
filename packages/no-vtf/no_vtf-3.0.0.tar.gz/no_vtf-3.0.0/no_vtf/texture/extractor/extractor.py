# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from collections.abc import Sequence
from typing import BinaryIO, Protocol, TypeVar, Union

_T_co = TypeVar("_T_co", covariant=True)


class TextureExtractor(Protocol[_T_co]):
    @abstractmethod
    def __call__(self, path_or_io: Union[pathlib.Path, BinaryIO], /) -> Sequence[_T_co]:
        ...
