# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import contextlib
import pathlib
import re

from collections.abc import Sequence
from typing import BinaryIO, ClassVar, Optional, Union

import kaitaistruct

from no_vtf.image.image import ImageDynamicRange
from no_vtf.parser.generated.vtf import Vtf as VtfParser
from no_vtf.texture.extractor.extractor import TextureExtractor
from no_vtf.texture.vtf import VtfTexture


class VtfExtractor(TextureExtractor[VtfTexture]):
    def __call__(self, path_or_io: Union[pathlib.Path, BinaryIO], /) -> Sequence[VtfTexture]:
        dynamic_range = None
        if isinstance(path_or_io, pathlib.Path):
            dynamic_range = self._guess_dynamic_range(path_or_io)

        context_manager: Union[BinaryIO, contextlib.AbstractContextManager[BinaryIO]] = (
            contextlib.nullcontext(path_or_io)
            if isinstance(path_or_io, BinaryIO)
            else open(path_or_io, "rb")
        )
        with context_manager as io:
            try:
                parser = VtfParser.from_io(io)
            except kaitaistruct.KaitaiStructError as exception:
                raise RuntimeError(f"Parser error: {exception}")

            high_res_image = self._high_res_image_7_0(parser) or self._high_res_image_7_3(parser)
            if not high_res_image:
                return []

            textures = self._textures_from_high_res_image(parser, high_res_image, dynamic_range)
            return textures

    _hdr_file_name_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"[_\.] \d*? hdr .*? \.vtf $", re.ASCII | re.IGNORECASE | re.VERBOSE
    )

    def _guess_dynamic_range(self, path: pathlib.Path) -> ImageDynamicRange:
        if self._hdr_file_name_pattern.search(path.name) is not None:
            return "hdr"
        else:
            return "ldr"

    def _high_res_image_7_0(self, parser: VtfParser) -> Optional[VtfParser.HighResImage]:
        return getattr(parser.body, "high_res_image", None)

    def _high_res_image_7_3(self, parser: VtfParser) -> Optional[VtfParser.HighResImage]:
        resources = getattr(parser.body, "resources", None)
        if not resources:
            return None

        for resource in resources:
            high_res_image: Optional[VtfParser.HighResImage] = getattr(
                resource, "high_res_image", None
            )
            if high_res_image:
                return high_res_image

        return None

    def _textures_from_high_res_image(
        self,
        parser: VtfParser,
        high_res_image: VtfParser.HighResImage,
        dynamic_range: Optional[ImageDynamicRange],
    ) -> list[VtfTexture]:
        is_cubemap = parser.header.logical.flags.envmap
        num_mipmaps = parser.header.v7_0.num_mipmaps
        num_frames = parser.header.v7_0.num_frames
        num_faces = parser.header.logical.num_faces
        num_slices = parser.header.logical.num_slices

        textures = []
        for mipmap_index, mipmap in enumerate(high_res_image.image_mipmaps):
            for frame_index, frame in enumerate(mipmap.image_frames):
                for face_index, face in enumerate(frame.image_faces):
                    for slice_index, image_slice in enumerate(face.image_slices):
                        texture = VtfTexture(
                            dynamic_range=dynamic_range,
                            is_cubemap=is_cubemap,
                            num_mipmaps=num_mipmaps,
                            num_frames=num_frames,
                            num_faces=num_faces,
                            num_slices=num_slices,
                            mipmap_index=mipmap_index,
                            frame_index=frame_index,
                            face_index=face_index,
                            slice_index=slice_index,
                            image=image_slice,
                        )
                        textures.append(texture)

        return textures
