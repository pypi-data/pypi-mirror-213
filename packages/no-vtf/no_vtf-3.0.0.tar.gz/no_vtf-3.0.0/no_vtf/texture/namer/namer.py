# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar

_T_contra = TypeVar("_T_contra", contravariant=True)


class TextureNamer(Protocol[_T_contra]):
    @abstractmethod
    def __call__(self, input_name: str, texture: _T_contra) -> str:
        ...
