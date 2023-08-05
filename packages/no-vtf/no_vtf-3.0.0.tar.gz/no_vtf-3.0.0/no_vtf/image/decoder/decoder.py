# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar

from no_vtf.image.image import Image, ImageDataTypes

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)


class ImageDecoder(Protocol[_I_co]):
    @abstractmethod
    def __call__(
        self, encoded_image: bytes, logical_width: int, logical_height: int, /
    ) -> Image[_I_co]:
        ...
