# -*- coding: utf-8 -*-
from outflow.core.pipeline import context
from outflow.core.logging import logger
from outflow.core.tasks import TaskManager
from outflow.core.types import Skipped


class Backend:
    def __init__(self):
        logger.debug(f"Initialize backend '{self}'")
        self.name = "default"

    def run(self, *, task_list):
        logger.debug(
            f"Run pipeline with backend '{self}' and with pipeline context '{context}'"
        )

        task_manager = TaskManager()

        for task in task_list:
            task.workflow.set_context(context)
            task_manager.compute(task.workflow)

        execution_return = [task_manager.results.resolve(task.id) for task in task_list]
        filter_results = False  # TODO parametrize outside
        if filter_results:
            return list(
                filter(
                    lambda el: not any(isinstance(val, Skipped) for val in el.values()),
                    execution_return,
                )
            )
        else:
            return execution_return

    def clean(self):
        pass
