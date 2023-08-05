# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Optional, TypeVar

import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    ByteOrder = np._ByteOrder
else:
    ByteOrder = Any

_S_co = TypeVar("_S_co", bound=np.generic, covariant=True)


def image_bytes_to_ndarray(
    image: bytes,
    width: int,
    height: int,
    channel_order: Sequence[int],
    scalar_type: type[_S_co],
    byte_order: Optional[ByteOrder] = None,
) -> npt.NDArray[_S_co]:
    num_channels = len(channel_order)
    shape = (height, width, num_channels)

    dtype = np.dtype(scalar_type)
    if byte_order is not None:
        dtype = dtype.newbyteorder(byte_order)

    ndarray: npt.NDArray[_S_co] = np.ndarray(shape=shape, dtype=dtype, buffer=image).copy()
    ndarray = ndarray[..., channel_order]
    return ndarray
