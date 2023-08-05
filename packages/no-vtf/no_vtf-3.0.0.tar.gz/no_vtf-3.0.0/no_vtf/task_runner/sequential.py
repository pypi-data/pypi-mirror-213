# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Iterable, Sequence
from typing import TypeVar, Union

from no_vtf.task_runner.task_runner import TaskRunner

_A_co = TypeVar("_A_co", covariant=True)


class SequentialRunner(TaskRunner):
    def __call__(
        self, tasks: Sequence[TaskRunner.Task[_A_co]]
    ) -> Iterable[tuple[TaskRunner.Task[_A_co], Union[_A_co, Exception]]]:
        for task in tasks:
            yield self.process(task)

    @staticmethod
    def process(
        task: TaskRunner.Task[_A_co],
    ) -> tuple[TaskRunner.Task[_A_co], Union[_A_co, Exception]]:
        try:
            result = task()
            return (task, result)
        except Exception as exception:
            return (task, exception)
