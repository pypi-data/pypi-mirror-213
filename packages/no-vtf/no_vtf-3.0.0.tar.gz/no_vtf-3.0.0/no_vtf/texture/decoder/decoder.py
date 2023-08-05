# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar

from no_vtf.image import Image, ImageDataTypes

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)


class TextureDecoder(Protocol[_T_contra, _I_co]):
    @abstractmethod
    def __call__(self, texture: _T_contra) -> Image[_I_co]:
        ...
