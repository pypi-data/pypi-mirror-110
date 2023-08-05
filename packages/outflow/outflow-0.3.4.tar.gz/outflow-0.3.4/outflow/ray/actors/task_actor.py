# -*- coding: utf-8 -*-
import ray

from .base_actor import BaseActor


@ray.remote
class TaskActor(BaseActor):
    def set_run(self, run_func):
        self.run_func = run_func

    def run(self, *args, **kwargs):
        return self.run_func(*args, **kwargs)
