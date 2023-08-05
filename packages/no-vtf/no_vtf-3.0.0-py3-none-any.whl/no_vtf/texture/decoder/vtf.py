# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools

from dataclasses import dataclass
from typing import Optional

from no_vtf.image import Image, ImageDataTypes, ImageDynamicRange
from no_vtf.image.decoder.decoder import ImageDecoder
from no_vtf.image.decoder.generic import (
    decode_a_uint8,
    decode_abgr_uint8,
    decode_argb_uint8,
    decode_bgr_uint8,
    decode_bgra_uint4_le,
    decode_bgra_uint8,
    decode_dxt1_rgb,
    decode_dxt1_rgba,
    decode_dxt3,
    decode_dxt5,
    decode_l_uint8,
    decode_la_uint8,
    decode_rgb_uint8,
    decode_rgba_float16_le,
    decode_rgba_uint8,
    decode_uv_uint8,
)
from no_vtf.image.decoder.vtf import (
    decode_bgr_uint8_bluescreen,
    decode_bgra_uint8_hdr,
    decode_rgb_uint8_bluescreen,
    decode_rgba_uint16_le_hdr,
)
from no_vtf.parser.generated.vtf import Vtf as VtfParser
from no_vtf.texture.decoder.decoder import TextureDecoder
from no_vtf.texture.vtf import VtfTexture


@dataclass(frozen=True, kw_only=True)
class VtfDecoder(TextureDecoder[VtfTexture, ImageDataTypes]):
    dynamic_range: Optional[ImageDynamicRange] = None
    overbright_factor: Optional[float] = None

    def __call__(self, texture: VtfTexture) -> Image[ImageDataTypes]:
        encoded_image = texture.image.image_data
        logical_width = texture.image.logical_width
        logical_height = texture.image.logical_height

        decoder = self._get_decoder(texture)
        decoded_image = decoder(encoded_image, logical_width, logical_height)
        return decoded_image

    def _get_decoder(self, texture: VtfTexture) -> ImageDecoder[ImageDataTypes]:
        image_format = texture.image.image_format

        dynamic_range = (
            self.dynamic_range if self.dynamic_range is not None else texture.dynamic_range
        )

        decoder: Optional[ImageDecoder[ImageDataTypes]] = None
        match (image_format, dynamic_range):
            case VtfParser.ImageFormat.rgba8888, _:
                decoder = decode_rgba_uint8
            case VtfParser.ImageFormat.abgr8888, _:
                decoder = decode_abgr_uint8
            case VtfParser.ImageFormat.rgb888, _:
                decoder = decode_rgb_uint8
            case VtfParser.ImageFormat.bgr888, _:
                decoder = decode_bgr_uint8
            case VtfParser.ImageFormat.i8, _:
                decoder = decode_l_uint8
            case VtfParser.ImageFormat.ia88, _:
                decoder = decode_la_uint8
            case VtfParser.ImageFormat.a8, _:
                decoder = decode_a_uint8
            case VtfParser.ImageFormat.rgb888_bluescreen, _:
                decoder = decode_rgb_uint8_bluescreen
            case VtfParser.ImageFormat.bgr888_bluescreen, _:
                decoder = decode_bgr_uint8_bluescreen
            case VtfParser.ImageFormat.argb8888, _:
                # VTFLib/VTFEdit, Gimp VTF Plugin, and possibly others, decode this format
                # differently because of mismatched channels (verified against VTF2TGA).
                decoder = decode_argb_uint8
            case VtfParser.ImageFormat.bgra8888, None:
                raise RuntimeError("Dynamic range is set neither on VtfTexture nor VtfDecoder")
            case VtfParser.ImageFormat.bgra8888, "ldr":
                decoder = decode_bgra_uint8
            case VtfParser.ImageFormat.bgra8888, "hdr":
                decoder = functools.partial(
                    decode_bgra_uint8_hdr, overbright_factor=self.overbright_factor
                )
            case VtfParser.ImageFormat.dxt1, _:
                decoder = decode_dxt1_rgb
            case VtfParser.ImageFormat.dxt3, _:
                decoder = decode_dxt3
            case VtfParser.ImageFormat.dxt5, _:
                decoder = decode_dxt5
            case VtfParser.ImageFormat.bgra4444, _:
                decoder = decode_bgra_uint4_le
            case VtfParser.ImageFormat.dxt1_onebitalpha, _:
                decoder = decode_dxt1_rgba
            case VtfParser.ImageFormat.uv88, _:
                decoder = decode_uv_uint8
            case VtfParser.ImageFormat.rgba16161616f, _:
                decoder = decode_rgba_float16_le
            case VtfParser.ImageFormat.rgba16161616, _:
                decoder = decode_rgba_uint16_le_hdr

        if not decoder:
            raise RuntimeError(f"Unsupported Valve texture format: {image_format.name}")

        return decoder
