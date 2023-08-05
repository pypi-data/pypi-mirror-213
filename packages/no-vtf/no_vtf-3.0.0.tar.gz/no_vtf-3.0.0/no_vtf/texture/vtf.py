# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import dataclasses

from dataclasses import dataclass
from typing import Optional

from no_vtf.image.image import ImageDynamicRange
from no_vtf.parser.generated.vtf import Vtf as VtfParser


@dataclass(frozen=True, kw_only=True)
class VtfTexture:
    dynamic_range: Optional[ImageDynamicRange]

    is_cubemap: bool

    num_mipmaps: int
    num_frames: int
    num_faces: int
    num_slices: int

    mipmap_index: int
    frame_index: int
    face_index: int
    slice_index: int

    image: VtfParser.Image = dataclasses.field(repr=False, hash=False)
