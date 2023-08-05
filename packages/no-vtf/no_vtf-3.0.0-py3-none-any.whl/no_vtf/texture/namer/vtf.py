# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass

from no_vtf.texture.namer.namer import TextureNamer
from no_vtf.texture.vtf import VtfTexture


@dataclass(frozen=True, kw_only=True)
class Vtf2TgaLikeNamer(TextureNamer[VtfTexture]):
    include_mipmap_level: bool

    def __call__(self, input_name: str, texture: VtfTexture) -> str:
        output_name = input_name

        if texture.is_cubemap:
            face_names = ("rt", "lf", "bk", "ft", "up", "dn", "sph")
            output_name += face_names[texture.face_index]

        if texture.num_frames > 1:
            output_name += f"{texture.frame_index:03d}"

        if self.include_mipmap_level and texture.num_mipmaps > 1:
            mipmap_level = texture.num_mipmaps - texture.mipmap_index - 1
            output_name += f"_mip{mipmap_level}"

        if texture.num_slices > 1:
            output_name += f"_z{texture.slice_index:03d}"

        return output_name
