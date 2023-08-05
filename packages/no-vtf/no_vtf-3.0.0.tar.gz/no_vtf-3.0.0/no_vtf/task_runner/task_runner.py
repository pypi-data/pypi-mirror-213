# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable, Sequence
from typing import ClassVar, Protocol, TypeVar, Union

import no_vtf.task_runner  # noqa: F401  # define all task runners for TaskRunner.initialize()

_A_co = TypeVar("_A_co", covariant=True)


class TaskRunner:
    class Task(Protocol[_A_co]):
        @abstractmethod
        def __call__(self) -> _A_co:
            ...

    _initialized: ClassVar[bool] = False

    @classmethod
    def initialize(cls) -> None:
        for subclass in cls.__subclasses__():
            subclass._initialize()

        cls._initialized = True

    @classmethod
    def _is_initialized(cls) -> bool:
        return cls._initialized

    @classmethod
    def _initialize(cls) -> None:
        pass

    @abstractmethod
    def __call__(
        self, tasks: Sequence[TaskRunner.Task[_A_co]]
    ) -> Iterable[tuple[TaskRunner.Task[_A_co], Union[_A_co, Exception]]]:
        ...
