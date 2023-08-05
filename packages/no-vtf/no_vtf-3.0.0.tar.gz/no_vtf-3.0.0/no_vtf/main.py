# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import contextlib
import inspect
import pathlib
import re
import sys

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, cast

import alive_progress
import click

import no_vtf

from no_vtf.filesystem import InputPaths, OutputDirectories
from no_vtf.image import ImageDataTypes, ImageDynamicRange
from no_vtf.pipeline import Pipeline
from no_vtf.task_runner import ParallelRunner, SequentialRunner, TaskRunner
from no_vtf.texture.decoder.vtf import VtfDecoder
from no_vtf.texture.extractor.vtf import VtfExtractor
from no_vtf.texture.filter.vtf import VtfMipmapFilter
from no_vtf.texture.namer.vtf import Vtf2TgaLikeNamer

_T = TypeVar("_T")


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf - Valve Texture Format Converter
    Copyright (C) 2023 b5327157

    https://sr.ht/~b5327157/no_vtf/
    https://pypi.org/project/no-vtf/

    This program is free software: you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    """

    click.echo(inspect.cleandoc(credits))
    ctx.exit()


@click.command(name="no_vtf", no_args_is_help=True)
@click.argument(
    "paths",
    metavar="PATH...",
    type=click.Path(path_type=pathlib.Path, exists=True),
    required=True,
    nargs=-1,
)
@click.option(
    "--output-dir",
    "-o",
    "output_directory",
    help="Output directory",
    type=click.Path(path_type=pathlib.Path, exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--ldr-format", "-l", help="LDR output format", show_default=True, type=str, default="tiff"
)
@click.option(
    "--hdr-format", "-h", help="HDR output format", show_default=True, type=str, default="exr"
)
@click.option(
    "--dynamic-range",
    "-d",
    help="Override LDR/HDR auto-detection",
    type=click.Choice(["ldr", "hdr"], case_sensitive=False),
)
@click.option(
    "--mipmaps",
    "-m",
    help="Extract all mipmaps",
    type=bool,
    is_flag=True,
)
@click.option(
    "--separate-channels",
    "-s",
    help="Output the RGB/L and A channels separately",
    type=bool,
    is_flag=True,
)
@click.option(
    "--overbright-factor",
    "-O",
    help="Multiplicative factor used for decoding compressed HDR textures",
    show_default=True,
    type=float,
    default=16,
)
@click.option(
    "--compress/--no-compress", help="Control lossless compression", type=bool, default=None
)
@click.option("write", "--always-write/--no-write", help="Write images", type=bool, default=None)
@click.option(
    "readback", "--readback/--no-readback", help="Readback images", type=bool, default=False
)
@click.option(
    "--num-workers",
    help="Number of workers for parallel conversion",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click.option(
    "--no-progress",
    help="Do not show the progress bar",
    type=bool,
    is_flag=True,
)
@click.version_option(version=no_vtf.__version__, message="%(version)s")
@click.option(
    "--credits",
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main_command(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    ldr_format: str,
    hdr_format: str,
    dynamic_range: Optional[ImageDynamicRange],
    mipmaps: bool,
    separate_channels: bool,
    overbright_factor: float,
    compress: Optional[bool],
    write: Optional[bool],
    readback: bool,
    num_workers: Optional[int],
    no_progress: bool,
) -> None:
    """
    Convert Valve Texture Format files into standard image files.

    PATH can be either file, or directory (in which case it is recursively searched
    for .vtf files, symbolic links are not followed). Multiple paths may be provided.

    If the output directory is not specified, images are output into the source directories.
    Otherwise, directory tree for any found files will be reconstructed in the chosen directory.

    Output LDR/HDR format is selected by its common file name extension.
    Special formats:
    "raw" to write the high resolution image data as-is;
    "skip" to skip the write step entirely.

    For supported formats, compression is controlled when saving the image.
    Lossless compression is enabled by default. Lossy compression is not used.

    The BGRA8888 format can store both LDR and compressed HDR images.
    The specific type is either auto-detected by looking at the input file name
    (roughly, if it contains "hdr" near the end), or can be set manually.

    Only the highest-resolution mipmap is extracted by default.
    Alternatively, all mipmaps of the high-resolution image can be extracted.

    The RGB/L and A channels are packed into one file by default.
    When output separately, resulting file names will be suffixed with "_rgb", "_l" or "_a".

    By default, image files are only written if they do not exist already.
    Alternatively, they can be overwritten, or writing can be disabled entirely.

    Images can be also read back to verify they have been written properly.
    Readback will error if data to be written do not match what is in the file.

    Worker is spawned for each logical core to run the conversion in parallel.
    Number of workers can be overridden. If set to 1, conversion is sequential.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    Upon a recoverable error, conversion will proceed with the next file.
    """

    main(
        paths=paths,
        output_directory=output_directory,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        dynamic_range=dynamic_range,
        mipmaps=mipmaps,
        separate_channels=separate_channels,
        overbright_factor=overbright_factor,
        compress=compress,
        write=write,
        readback=readback,
        num_workers=num_workers,
        no_progress=no_progress,
    )


def main(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    ldr_format: str,
    hdr_format: str,
    dynamic_range: Optional[ImageDynamicRange],
    mipmaps: bool,
    separate_channels: bool,
    overbright_factor: float,
    compress: Optional[bool],
    write: Optional[bool],
    readback: bool,
    num_workers: Optional[int],
    no_progress: bool,
) -> None:
    vtf_extension_pattern = re.compile(r"\.vtf$", re.ASCII | re.IGNORECASE)

    texture_extractor = VtfExtractor()
    texture_filter = VtfMipmapFilter(mipmap_levels=slice(-1, None)) if not mipmaps else None
    texture_decoder = VtfDecoder(dynamic_range=dynamic_range, overbright_factor=overbright_factor)
    texture_namer = Vtf2TgaLikeNamer(include_mipmap_level=mipmaps)

    Pipeline.initialize()
    pipeline = Pipeline(
        input_extension_pattern=vtf_extension_pattern,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        separate_channels=separate_channels,
        compress=compress,
        write=write,
        readback=readback,
        extractor=texture_extractor,
        filter=texture_filter,
        decoder=texture_decoder,
        namer=texture_namer,
    )

    input_paths = InputPaths(paths)
    if input_paths.has_directories():
        _resolve_directories(input_paths, not no_progress)

    task_runner: TaskRunner
    if num_workers is None or num_workers > 1:
        task_runner = ParallelRunner(max_workers=num_workers, initializer=Pipeline.initialize)
    else:
        task_runner = SequentialRunner()

    tasks = _get_tasks(pipeline, input_paths, output_directory)
    exit_status = _process_tasks(task_runner, tasks, not no_progress)
    sys.exit(exit_status)


def _resolve_directories(input_paths: InputPaths, show_progress: bool) -> None:
    progress_bar_manager = (
        alive_progress.alive_bar(receipt=False, spinner=None, theme="classic", enrich_print=False)
        if show_progress
        else None
    )
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for file in input_paths.search_in_directories("*.[vV][tT][fF]", add_results=True):
            if progress_bar:
                progress_bar.text = file.name
                progress_bar()
        input_paths.remove_directories()


def _get_tasks(
    pipeline: Pipeline[_T, ImageDataTypes],
    input_paths: InputPaths,
    output_directory: Optional[pathlib.Path],
) -> Sequence[_Task[_T]]:
    output_directories = OutputDirectories(output_directory)

    tasks: list[_Task[_T]] = []
    for input_file, input_base_directory in input_paths:
        output_directory = output_directories(input_file, input_base_directory)
        task = _Task(pipeline=pipeline, input_file=input_file, output_directory=output_directory)
        tasks.append(task)
    return tasks


def _process_tasks(
    task_runner: TaskRunner,
    tasks: Sequence[_Task[_T]],
    show_progress: bool,
) -> int:
    exit_status = 0

    num_files = len(tasks)
    progress_bar_manager = (
        alive_progress.alive_bar(num_files, spinner=None, theme="classic", enrich_print=False)
        if show_progress
        else None
    )
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for task, result in task_runner(tasks):
            task = cast(_Task[_T], task)
            if isinstance(result, Pipeline.Receipt):
                if progress_bar:
                    skipped = not result.io_done
                    progress_bar(skipped=skipped)
                    progress_bar.text = str(task.input_file)
            else:
                exit_status = 1

                exception: Exception = result
                message = f"Error while processing {task!r}: {exception}"
                if exception.__cause__:
                    message += f" ({exception.__cause__})"
                click.echo(message, file=sys.stderr)

    return exit_status


@dataclass(frozen=True, kw_only=True)
class _Task(Generic[_T], TaskRunner.Task[Pipeline.Receipt]):
    pipeline: Pipeline[_T, ImageDataTypes]
    input_file: pathlib.Path
    output_directory: pathlib.Path

    def __call__(self) -> Pipeline.Receipt:
        return self.pipeline(self.input_file, output_directory=self.output_directory)

    def __str__(self) -> str:
        return f"{self.input_file}"

    def __repr__(self) -> str:
        return f"{self.input_file!r}"
