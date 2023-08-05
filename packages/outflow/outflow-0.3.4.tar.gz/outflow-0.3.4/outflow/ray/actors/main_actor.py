# -*- coding: utf-8 -*-

import ray
from outflow.ray.task_manager import RayTaskManager

from .base_actor import BaseActor


@ray.remote
class MainActor(BaseActor):
    def run(self, *, task_list):

        # logger.debug(
        #     f"Run pipeline with actor '{self}' and with pipeline context '{self.pipeline_context}'"
        # )
        task_manager = RayTaskManager()

        for task in task_list:
            # task.workflow.set_context(self.pipeline_context)
            task_manager.compute(task.workflow)

        return [task_manager.results.resolve(task.id) for task in task_list]
