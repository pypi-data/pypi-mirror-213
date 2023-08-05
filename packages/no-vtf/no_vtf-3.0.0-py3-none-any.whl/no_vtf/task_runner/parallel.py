# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import multiprocessing
import signal

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Optional, TypeVar, Union

from no_vtf.task_runner.sequential import SequentialRunner
from no_vtf.task_runner.task_runner import TaskRunner

_A_co = TypeVar("_A_co", covariant=True)


@dataclass(frozen=True, kw_only=True)
class ParallelRunner(TaskRunner):
    max_workers: Optional[int] = None
    initializer: Optional[Callable[[], None]] = None

    @classmethod
    def _initialize(cls) -> None:
        multiprocessing.freeze_support()

    def __post_init__(self) -> None:
        assert self._is_initialized(), "TaskRunner.initialize() must be called early"

    def __call__(
        self, tasks: Sequence[TaskRunner.Task[_A_co]]
    ) -> Iterable[tuple[TaskRunner.Task[_A_co], Union[_A_co, Exception]]]:
        initializer = functools.partial(ParallelRunner._worker_initializer, self.initializer)
        with multiprocessing.Pool(self.max_workers, initializer=initializer) as pool:
            for task, result in pool.imap_unordered(SequentialRunner.process, tasks):
                yield (task, result)

    @staticmethod
    def _worker_initializer(additional_initializer: Optional[Callable[[], None]]) -> None:
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        if additional_initializer:
            additional_initializer()
