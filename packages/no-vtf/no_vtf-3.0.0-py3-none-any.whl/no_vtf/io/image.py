# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import functools
import pathlib
import re

from dataclasses import dataclass
from typing import ClassVar, Optional, cast

import imageio.plugins.freeimage
import imageio.v3
import numpy as np
import numpy.typing as npt

from no_vtf.image import Image, ImageData, ImageDataTypes
from no_vtf.image.modifier.fp_precision_modifier import FPPrecisionModifier
from no_vtf.image.modifier.modifier import ImageModifier
from no_vtf.io.io import IO


@dataclass(frozen=True, kw_only=True)
class ImageIO(IO[Image[ImageDataTypes]]):
    format: str

    compress: Optional[bool] = None

    @classmethod
    def _initialize(cls) -> None:
        # download() seems to be untyped because of implicit reexport
        imageio.plugins.freeimage.download()  # type: ignore[no-untyped-call]

    _format_pattern: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9]+", re.ASCII | re.IGNORECASE)

    def __post_init__(self) -> None:
        assert self._is_initialized(), "IO.initialize() must be called early"

        if not self._format_pattern.fullmatch(self.format):
            raise RuntimeError(f"Invalid format: {self.format}")

    def write(self, path: pathlib.Path, image: Image[ImageDataTypes]) -> None:
        backend = self._get_backend()
        backend.write(path, image)

    def readback(self, path: pathlib.Path, image: Image[ImageDataTypes]) -> None:
        backend = self._get_backend()
        backend.readback(path, image)

    def _get_backend(self) -> _ImageIOBackend:
        compress = self.compress
        if compress is None:
            compress = True

        extension = f".{self.format}"

        backend: _ImageIOBackend
        match self.format.lower():
            case "exr":
                backend = _ImageIOExrBackend(compress=compress)
            case "png":
                backend = _ImageIOPngBackend(compress=compress)
            case "targa" | "tga":
                backend = _ImageIOTgaBackend(compress=compress)
            case "tiff":
                backend = _ImageIOTiffBackend(compress=compress)
            case _:
                backend = _ImageIOBackend(extension=extension)
        return backend


class _ImageIOBackend:
    def __init__(
        self, *, imageio_format: Optional[str] = None, extension: Optional[str] = None
    ) -> None:
        self._imageio_format = imageio_format
        self._extension = extension

    def write(self, path: pathlib.Path, image: Image[ImageDataTypes]) -> None:
        kwargs = self._get_writer_kwargs(image)
        image = self._postprocess(image)
        data = self._get_data(image)

        legacy_opener = functools.partial(imageio.v3.imopen, legacy_mode=True)
        with legacy_opener(
            path, "w", plugin=self._imageio_format, extension=self._extension
        ) as image_resource:
            image_resource.write(data, **kwargs)

    def readback(self, path: pathlib.Path, image: Image[ImageDataTypes]) -> None:
        image = self._postprocess(image)
        data = self._get_data(image)

        legacy_opener = functools.partial(imageio.v3.imopen, legacy_mode=True)
        with legacy_opener(
            path, "r", plugin=self._imageio_format, extension=self._extension
        ) as image_resource:
            read_data = image_resource.read(index=0)

            if data.dtype != read_data.dtype:
                raise RuntimeError(f"{path!r}: Data type differs from what is in the file")

            if not self._compare_data(data, read_data):
                raise RuntimeError(f"{path!r}: Data differs from what is in the file")

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        return {}

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return image

    def _get_data(self, image: Image[ImageDataTypes]) -> ImageData:
        data = image.data()

        # write luminance into three channels when alpha is present
        if image.channels == "la":
            l_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [0]]
            a_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [1]]
            data = np.dstack((l_uint8, l_uint8, l_uint8, a_uint8))

        # remove last axis if its length is 1
        if data.shape[-1] == 1:
            data = data[..., 0]

        return data

    def _compare_data(self, data: ImageData, read_data: ImageData) -> bool:
        return np.array_equal(data, read_data)


class _ImageIOFreeImageBackend(_ImageIOBackend):
    IO_FLAGS: ClassVar = imageio.plugins.freeimage.IO_FLAGS

    def __init__(self, *, imageio_format: str, extension: str) -> None:
        super().__init__(imageio_format=imageio_format, extension=extension)

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs: dict[str, object] = {}
        kwargs["flags"] = self._get_flags(image)
        return kwargs

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        return 0


class _ImageIOExrBackend(_ImageIOFreeImageBackend):
    _fp_force_32_bits: ClassVar[
        ImageModifier[ImageDataTypes, ImageDataTypes]
    ] = FPPrecisionModifier(min=32, max=32)

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="EXR-FI", extension=".exr")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.EXR_ZIP if self.compress else self.IO_FLAGS.EXR_NONE
        if not np.issubdtype(image.data().dtype, np.float16):
            flags |= self.IO_FLAGS.EXR_FLOAT
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return self._fp_force_32_bits(image)


class _ImageIOPngBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="PNG-FI", extension=".png")
        self.compress = compress

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs: dict[str, object] = super()._get_writer_kwargs(image)
        kwargs["compression"] = 1 if self.compress else 0
        return kwargs

    def _compare_data(self, data: ImageData, read_data: ImageData) -> bool:
        if np.issubdtype(data.dtype, np.uint8) and np.issubdtype(read_data.dtype, np.uint8):
            if read_data.ndim == 3 and read_data.shape[2] == 3:
                data = _strip_opaque_alpha(cast(npt.NDArray[np.uint8], data))

        return super()._compare_data(data, read_data)


class _ImageIOTgaBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TARGA-FI", extension=".tga")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TARGA_SAVE_RLE if self.compress else self.IO_FLAGS.TARGA_DEFAULT
        return flags


class _ImageIOTiffBackend(_ImageIOFreeImageBackend):
    _fp_force_32_bits: ClassVar[
        ImageModifier[ImageDataTypes, ImageDataTypes]
    ] = FPPrecisionModifier(min=32, max=32)

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TIFF-FI", extension=".tiff")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TIFF_DEFAULT if self.compress else self.IO_FLAGS.TIFF_NONE
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return self._fp_force_32_bits(image)


def _strip_opaque_alpha(data: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    if data.ndim == 3 and data.shape[2] == 4 and np.all(data[..., 3] == 255):
        data = data[..., :3]

    return data
