# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypeAlias, TypeVar, Union

import numpy as np
import numpy.typing as npt

from no_vtf.deferred import Deferred

ImageDataTypesLDR: TypeAlias = np.uint8 | np.uint16
ImageDataTypesHDR: TypeAlias = np.float16 | np.float32

ImageDataTypes: TypeAlias = Union[ImageDataTypesLDR, ImageDataTypesHDR]

ImageData: TypeAlias = npt.NDArray[ImageDataTypes]

ImageChannels = Literal["rgb", "rgba", "l", "la", "a"]
ImageDynamicRange = Literal["ldr", "hdr"]

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)


@dataclass(frozen=True, kw_only=True)
class Image(Generic[_I_co]):
    raw: Optional[bytes]

    data: Deferred[npt.NDArray[_I_co]]
    dtype: npt.DTypeLike
    channels: ImageChannels

    @property
    def dynamic_range(self) -> ImageDynamicRange:
        ldr = _is_ldr(self.dtype)
        hdr = _is_hdr(self.dtype)
        assert ldr != hdr, "_is_ldr() and _is_hdr() must be mutually exclusive"

        return "hdr" if hdr else "ldr"


def _is_ldr(dtype: npt.DTypeLike) -> bool:
    ldr_dtypes = typing.get_args(ImageDataTypesLDR)
    return any(np.issubdtype(dtype, ldr_dtype) for ldr_dtype in ldr_dtypes)


def _is_hdr(dtype: npt.DTypeLike) -> bool:
    hdr_dtypes = typing.get_args(ImageDataTypesHDR)
    return any(np.issubdtype(dtype, hdr_dtype) for hdr_dtype in hdr_dtypes)
