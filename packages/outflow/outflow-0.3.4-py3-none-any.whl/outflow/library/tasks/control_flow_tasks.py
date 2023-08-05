# -*- coding: utf-8 -*-
from typing import Callable

from outflow.core.tasks import Task
from outflow.core.types import Skipped


class IdentityTask(Task):
    """Important : when implementing an IdentityTask, make sure the self.run()
    function ends with `return kwargs`
    TODO: Change the name of this task because it is not really an "identity" as we are allowed to mutate kwargs
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, auto_outputs=False, **kwargs)

    def add_parent(self, parent_task):
        super().add_parent(parent_task)
        self.copy_targets(parent_task)

    def copy_targets(self, task):
        self.inputs.update(task.outputs)
        self.outputs.update(task.outputs)

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def run(self, **kwargs):
        return kwargs


class ConditionalTask(IdentityTask):
    def __init__(self, condition: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._condition = condition

    def condition(self, **kwargs):
        try:
            condition_result = self._condition(self, **kwargs)
        except TypeError as te:
            raise TypeError(
                te.__str__()
                + ". Make sure the first argument of your condition is the task."
            ) from te
        return condition_result


class IfTask(ConditionalTask):
    def run(self, *args, **kwargs):
        if not self.condition(**kwargs):
            for child_task in self.children:
                child_task.skip = True
        else:
            return super().run(**kwargs)


class ElseTask(ConditionalTask):
    def run(self, **kwargs):
        if self.condition(**kwargs):
            for child_task in self.children:
                child_task.skip = True
        else:
            return super().run(**kwargs)


def IfElse(condition: Callable, name: str = "ConditionalTask"):
    # subclass if/else task to avoid edge effects with targets and other class attributes
    IfSubClass = type("If" + name, (IfTask,), {})
    ElseSubClass = type("Else" + name, (ElseTask,), {})
    return IfSubClass(condition), ElseSubClass(condition)


class MergeTask(IdentityTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_if_upstream_skip = False

    def __call__(self, *args, **kwargs):
        if all(parent.skip for parent in self.parents):
            self.skip = True

        return super().__call__(*args, **kwargs)

    def run(self, **kwargs):

        not_none_inputs = {
            key: val
            for key, val in kwargs.items()
            if val is not None and not isinstance(val, Skipped)
        }

        stripped_return_dict = {}

        # TODO: maybe check if all inputs start with the same name

        for output in self.outputs:
            for input_name, input_val in not_none_inputs.items():
                if input_name.endswith(output):
                    stripped_return_dict.update({output: input_val})

        return stripped_return_dict
