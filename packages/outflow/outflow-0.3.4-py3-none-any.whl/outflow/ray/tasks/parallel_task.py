# -*- coding: utf-8 -*-
import sys

from outflow.core.pipeline import get_pipeline_states
from outflow.core.tasks import BaseTask
from outflow.ray.actors import TaskActor


class ParallelTask(BaseTask):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        super().__call__()
        self.actor = TaskActor.options(
            resources={"head_node": 1}, num_cpus=self.num_cpus
        ).remote(pipeline_states=get_pipeline_states(), python_path=sys.path)
        self.actor.set_run.remote(self.run)
        actor_result = self.actor.run.remote(
            **kwargs, **self.bind_kwargs, **self.parameterized_kwargs
        )

        return actor_result
