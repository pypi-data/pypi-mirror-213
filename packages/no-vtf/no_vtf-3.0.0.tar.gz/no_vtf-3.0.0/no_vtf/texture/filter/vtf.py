# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from no_vtf.texture.filter.filter import TextureFilter
from no_vtf.texture.vtf import VtfTexture


@dataclass(frozen=True, kw_only=True)
class VtfMipmapFilter(TextureFilter[VtfTexture]):
    mipmap_levels: slice

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if not textures:
            return []

        assert (
            len(set(map(lambda texture: texture.num_mipmaps, textures))) == 1
        ), "num_mipmaps must be the same for all filtered textures"
        indices = range(*self.mipmap_levels.indices(textures[0].num_mipmaps))

        textures = list(filter(lambda texture: texture.mipmap_index in indices, textures))
        return textures


@dataclass(frozen=True, kw_only=True)
class VtfResolutionFilter(TextureFilter[VtfTexture]):
    min: Optional[int] = None
    max: Optional[int] = None

    closest_as_fallback: bool = False

    def __post_init__(self) -> None:
        if self.min is not None and self.max is not None and self.min > self.max:
            raise RuntimeError(f"Unordered resolutions: {self.min = } <= {self.max = }")

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if self.min is None and self.max is None:
            return textures

        def resolution_filter(texture: VtfTexture) -> bool:
            if self.min is not None:
                if not all(
                    resolution >= self.min
                    for resolution in (texture.image.logical_width, texture.image.logical_height)
                ):
                    return False

            if self.max is not None:
                if not all(
                    resolution <= self.max
                    for resolution in (texture.image.logical_width, texture.image.logical_height)
                ):
                    return False

            return True

        exact_matches = list(filter(resolution_filter, textures))
        if exact_matches or not self.closest_as_fallback:
            return exact_matches

        assert (
            self.min is not None or self.max is not None
        ), "either min or max resolution must be set"
        num_pixels = (self.min or self.max or 0) * (self.max or self.min or 0)

        close_matches = {
            abs(num_pixels - texture.image.logical_width * texture.image.logical_height): texture
            for texture in textures
        }
        close_matches = dict(sorted(close_matches.items()))

        closest_match = list(close_matches.values())[0:1]
        return closest_match
