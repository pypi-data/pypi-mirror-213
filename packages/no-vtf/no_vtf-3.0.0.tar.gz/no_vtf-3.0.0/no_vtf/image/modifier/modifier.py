# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar, Union

from no_vtf.image import Image, ImageDataTypes

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)
_I_contra = TypeVar("_I_contra", bound=ImageDataTypes, contravariant=True)


class ImageModifier(Protocol[_I_contra, _I_co]):
    @abstractmethod
    def __call__(self, image: Image[_I_contra], /) -> Image[Union[_I_contra, _I_co]]:
        ...
