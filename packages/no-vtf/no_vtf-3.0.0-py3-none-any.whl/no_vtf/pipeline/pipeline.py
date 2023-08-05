# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import pathlib
import re

from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypeVar, overload

from no_vtf.image.channel_separator import ChannelSeparator
from no_vtf.image.image import Image, ImageDataTypes
from no_vtf.io.bytes import BytesIO
from no_vtf.io.image import ImageIO
from no_vtf.io.io import IO
from no_vtf.texture.decoder.decoder import TextureDecoder
from no_vtf.texture.extractor.extractor import TextureExtractor
from no_vtf.texture.filter.filter import TextureFilter
from no_vtf.texture.namer.namer import TextureNamer

_A_contra = TypeVar("_A_contra", contravariant=True)
_I = TypeVar("_I", bound=ImageDataTypes)
_T = TypeVar("_T")


@dataclass(frozen=True, kw_only=True)
class Pipeline(Generic[_T, _I]):
    @dataclass(frozen=True, kw_only=True)
    class Receipt:
        io_done: bool

    input_extension_pattern: Optional[re.Pattern[str]] = None

    FORMAT_RAW: Literal["raw"] = "raw"
    FORMAT_SKIP: Literal["skip"] = "skip"
    ldr_format: str
    hdr_format: str

    separate_channels: bool = False

    compress: Optional[bool] = None

    write: Optional[bool] = None
    readback: bool = False

    extractor: TextureExtractor[_T]
    filter: Optional[TextureFilter[_T]]
    decoder: TextureDecoder[_T, _I]
    namer: TextureNamer[_T]

    @classmethod
    def initialize(cls) -> None:
        IO.initialize()

    @overload
    def __call__(self, input_file: pathlib.Path, *, output_file: pathlib.Path) -> Pipeline.Receipt:
        ...

    @overload
    def __call__(
        self, input_file: pathlib.Path, *, output_directory: pathlib.Path
    ) -> Pipeline.Receipt:
        ...

    def __call__(
        self,
        input_file: pathlib.Path,
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> Pipeline.Receipt:
        io_done = False

        textures = self.extractor(input_file)

        if self.filter:
            textures = self.filter(textures)

        for texture in textures:
            image = self.decoder(texture)

            image_format = self.hdr_format if image.dynamic_range == "hdr" else self.ldr_format
            if _compare_formats(image_format, self.FORMAT_SKIP):
                continue

            texture_output_file = output_file
            if texture_output_file is None:
                assert output_directory is not None, "output path must be set"

                input_name = input_file.name
                if self.input_extension_pattern:
                    input_name = re.sub(self.input_extension_pattern, "", input_name)

                texture_name = self.namer(input_name, texture)
                texture_output_name = texture_name + "." + image_format
                texture_output_file = output_directory / texture_output_name

            if _compare_formats(image_format, self.FORMAT_RAW):
                assert image.raw, "image must have raw data set"
                io_done = self._do_io(BytesIO(), texture_output_file, image.raw) or io_done
            else:
                image_io = ImageIO(format=image_format, compress=self.compress)
                if not self.separate_channels:
                    io_done = self._do_io(image_io, texture_output_file, image) or io_done
                else:
                    io_done = (
                        self._separate_channels(image_io, texture_output_file, image) or io_done
                    )

        return Pipeline.Receipt(io_done=io_done)

    def _separate_channels(
        self, image_io: ImageIO, path: pathlib.Path, image: Image[ImageDataTypes]
    ) -> bool:
        io_done = False

        channel_separator = ChannelSeparator()
        for image_separated in channel_separator(image):
            new_stem = path.stem + "_" + image_separated.channels
            new_path = path.with_stem(new_stem)
            io_done = self._do_io(image_io, new_path, image_separated) or io_done

        return io_done

    def _do_io(self, io: IO[_A_contra], path: pathlib.Path, data: _A_contra) -> bool:
        io_done = False

        if self.write is not False:
            io_done = self._write(io, path, data) or io_done

        if self.readback:
            io.readback(path, data)
            io_done = True

        return io_done

    def _write(self, io: IO[_A_contra], path: pathlib.Path, data: _A_contra) -> bool:
        assert self.write is not False, "_write() must not be called when writing is disabled"
        skip_existing = self.write is None
        if skip_existing and path.is_file():
            return False

        path.parent.mkdir(parents=True, exist_ok=True)
        io.write(path, data)

        return True


def _compare_formats(a: str, b: str) -> bool:
    return a.lower() == b.lower()
