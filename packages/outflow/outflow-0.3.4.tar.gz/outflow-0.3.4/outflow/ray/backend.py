# -*- coding: utf-8 -*-
import multiprocessing
import os
import platform
import subprocess
import sys
import tempfile
import threading
import time

from outflow.core.backends.backend import Backend as DefaultBackend
from outflow.core.logging import logger
from outflow.core.logging import LogRecordSocketReceiver
from outflow.ray.actors import MainActor
from outflow.core.pipeline import config, get_pipeline_states, context

import ray


class Backend(DefaultBackend):
    def __init__(self, num_cpus=1, resources={"head_node": 1}):
        super().__init__()
        self._job_ids_queue = None
        self.num_nodes = 0
        self.head_node_params = dict()
        self.workers_params = dict()
        self.setup_cluster()
        self.ray_actor = MainActor.options(resources=resources, num_cpus=num_cpus)
        self.tcpserver = LogRecordSocketReceiver()
        self.name = "ray"
        self.init_tcp_socket_receiver()
        self.stop_event = None
        self.sbatch_proc = None

    @property
    def job_ids_queue(self):
        if self._job_ids_queue is None:
            self._job_ids_queue = multiprocessing.Queue()

        return self._job_ids_queue

    @staticmethod
    def launch_nodes(
        workers_params: dict,
        num_nodes: int,
        job_ids_q: multiprocessing.Queue,
        stop_event: multiprocessing.Event,
    ):
        # subprocess local imports
        from outflow.core.logging import logger
        from simple_slurm import Slurm

        # redirect logs from subprocess to logger
        # sys.stdout = StreamToLogger(logger)

        ray_node = Slurm(
            cpus_per_task=workers_params["cpu_per_node"],
            mem=workers_params["mem_per_node"],
            job_name="ray_node",
        )

        for index in range(num_nodes):
            if index > 0:
                time.sleep(3)

            if stop_event.is_set():
                return

            python_path = sys.executable

            sbatch = (
                "srun {python_path} -m ray.scripts.scripts start --block --address='{redis_address}' "
                "--num-cpus={cpu_per_node} "
                "--redis-password='{_redis_password}'".format(
                    python_path=python_path,
                    **workers_params,
                )
            )
            logger.debug(f"calling sbatch with : {sbatch}")

            job_ids_q.put(ray_node.sbatch(sbatch))

    def setup_cluster(self):
        """
        Starts the ray head server, the main worker and sbatch the nodes
        """
        import ray

        # shutdown ray to avoid re-init issues
        ray.shutdown()

        # launch ray head server and main worker

        cluster_config = config.get("cluster", {})

        if "mem_per_node" in cluster_config:
            # --- Binary ---
            # 1 MiB = 1024 * 1024
            # 1 MiB = 2^20 bytes = 1 048 576 bytes = 1024 kibibytes
            # 1024 MiB = 1 gibibyte (GiB)

            # --- Decimal ---
            # 1 MB = 1^3 kB = 1 000 000 bytes

            self.workers_params.update({"mem_per_node": cluster_config["mem_per_node"]})
        if "cpu_per_node" in cluster_config:
            self.workers_params.update({"cpu_per_node": cluster_config["cpu_per_node"]})

        self.workers_params.update(
            {"_redis_password": cluster_config.get("redis_password", "outflow")}
        )
        self.head_node_params.update(
            {"_redis_password": self.workers_params["_redis_password"]}
        )

        # FIXME: fix ray to support parallel job on windows
        if platform.system() == "Windows" or config["local_mode"]:
            self.head_node_params.update({"local_mode": True})

        # needed when plugins are not installed but only in python path
        os.environ["PYTHONPATH"] = ":".join(sys.path)

        temp_dir = tempfile.mkdtemp(prefix="outflow_ray_")
        self.head_node_params.update({"_temp_dir": temp_dir})
        self.head_node_params.update({"num_cpus": 1})
        ray_info = ray.init(
            **self.head_node_params,
            resources={"head_node": 1e5},
            object_store_memory=1000000000
            # log_to_driver=False,
        )

        self.workers_params.update({"redis_address": ray_info["redis_address"]})
        context.redis_address = ray_info["redis_address"].split(":")[0]

        self.num_nodes = cluster_config.get("num_nodes", 0)

    def init_tcp_socket_receiver(self):
        logger.debug("About to start TCP server...")

        self.server_thread = threading.Thread(target=self.tcpserver.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()

    def run(self, *, task_list=[]):
        self.ray_actor = self.ray_actor.remote(
            pipeline_states=get_pipeline_states(), python_path=sys.path
        )
        main_actor_result = self.ray_actor.run.remote(task_list=task_list)
        result = -1

        if self.num_nodes > 0:
            self.stop_event = multiprocessing.Event()
            logger.info(f"Launching {self.num_nodes} ray nodes")

            self.sbatch_proc = multiprocessing.Process(
                target=self.launch_nodes,
                args=(
                    self.workers_params,
                    self.num_nodes,
                    self.job_ids_queue,
                    self.stop_event,
                ),
            )
            self.sbatch_proc.start()

        else:
            logger.info(
                "No cluster config found in configuration file, "
                "running in a local cluster"
            )

        # main call to the pipeline execution
        result = ray.get(main_actor_result)
        return result

    def clean(self):

        logger.debug("Cleaning ray backend")
        self.tcpserver.shutdown()

        if self.num_nodes > 0:
            if self.stop_event:
                self.stop_event.set()
            if self.sbatch_proc:
                self.sbatch_proc.join()

            while not self.job_ids_queue.empty():
                slurm_id = self.job_ids_queue.get()
                logger.debug("cancelling slurm id {id}".format(id=slurm_id))
                subprocess.run(["scancel", str(slurm_id)])

        ray.shutdown()
