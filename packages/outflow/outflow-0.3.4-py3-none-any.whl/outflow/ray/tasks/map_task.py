# -*- coding: utf-8 -*-
import sys
from typing import List

import ray

from outflow.core.target import Target
from outflow.core.tasks import Task
from outflow.core.types import IterateOn
from outflow.ray.actors import MapActor
from outflow.core.pipeline import get_pipeline_states


class MapTask(Task):
    def __init__(
        self,
        start: Task,
        *,
        end: Task = None,
        name=None,
        reduce_func=None,
        outputs=None,
        output_name="map_output",
        num_cpus=1,
        raise_exceptions=False
    ):
        super().__init__(auto_outputs=False)
        if outputs is None:
            self.outputs = {output_name: Target(output_name, type=List)}
        else:
            self.outputs = outputs

        input_targets = [target for target in start.inputs.values()]
        self.inputs = {
            target.type.__name__[len(IterateOn.prefix) :]
            if target.type.__name__.startswith(IterateOn.prefix)
            else target.name: target
            for target in input_targets
        }

        if name is not None:
            self.name = name

        self.start = start

        if end is None:
            self.start.terminating = True
            self.end = self.start
        else:
            end.terminating = True
            self.end = end

        if reduce_func is None:
            self.reduce = lambda x: {output_name: x}
        self.raise_exceptions = raise_exceptions
        self.num_cpus = num_cpus

    def run(self, **map_inputs):

        loop_workflow = self.start.workflow
        loop_workflow.start = self.start

        actor_results = list()

        for index, generated_inputs in enumerate(self.generator(**map_inputs)):
            # ensure the workflow start is the given task
            actor = MapActor.options(num_cpus=self.num_cpus).remote(
                loop_workflow,
                generated_inputs,
                index,
                self.raise_exceptions,
                pipeline_states=get_pipeline_states(),
                python_path=sys.path,
            )

            actor_results.append(actor.run.remote())

        result = [
            objid for sublist in ray.get(actor_results) for objid in sublist
        ]  # TODO remove this
        return self.reduce(result)

    def generator(self, **map_inputs):
        """
        default generator function
        :param map_inputs:
        :return:
        """

        not_iterable_inputs = map_inputs.copy()

        iterable_targets = [
            target
            for target, target in self.start.inputs.items()
            if target.type.__name__.startswith(IterateOn.prefix)
        ]

        # sequence_input_names = []
        input_names = []
        sequences = []

        for iterable_target in iterable_targets:

            # get the input name of the sequence to map
            sequence_input_name = iterable_target.type.__name__[len(IterateOn.prefix) :]
            # sequence_input_names.append(sequence_input_name)
            input_names.append(iterable_target.name)
            sequences.append(map_inputs[sequence_input_name])

            del not_iterable_inputs[sequence_input_name]

        for input_values in zip(*sequences):
            vals = {input_names[i]: input_values[i] for i in range(len(input_names))}
            yield {**vals, **not_iterable_inputs}
