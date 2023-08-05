# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass
from typing import Literal, Optional, TypeVar, Union

import numpy as np

from no_vtf.image import Image, ImageDataTypes
from no_vtf.image.modifier import ImageModifier

FloatingPointNumBits = Literal[16, 32, 64]

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)
_I_contra = TypeVar("_I_contra", bound=ImageDataTypes, contravariant=True)


@dataclass(frozen=True, kw_only=True)
class FPPrecisionModifier(ImageModifier[_I_contra, _I_co]):
    min: Optional[FloatingPointNumBits] = None
    max: Optional[FloatingPointNumBits] = None

    def __post_init__(self) -> None:
        if self.min is not None and self.max is not None and self.min > self.max:
            raise RuntimeError(f"Unordered precisions: {self.min = } <= {self.max = }")

    def __call__(self, image: Image[_I_contra]) -> Image[Union[_I_contra, _I_co]]:
        if not np.issubdtype(image.dtype, np.floating):
            return image

        fp_bits = np.dtype(image.dtype).itemsize * 8

        if self.min is not None and fp_bits < self.min:
            dtype = f"float{self.min}"
            data = image.data.map(lambda data: data.astype(dtype))
            return Image(raw=None, data=data, dtype=dtype, channels=image.channels)

        if self.max is not None and fp_bits > self.max:
            dtype = f"float{self.max}"
            data = image.data.map(lambda data: data.astype(dtype))
            return Image(raw=None, data=data, dtype=dtype, channels=image.channels)

        return image
