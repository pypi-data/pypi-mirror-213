import aiohttp
import asyncio
import functools
import json
import platform
import socket
import subprocess
from typing import List, Optional
import atexit
import random
import requests
import tempfile

from launch.prometheus import queries

RAY_CLUSTER_ADDRESS = "http://127.0.0.1:8265"
LAUNCHFLOW_PROM_CONTAINER_NAME = "launchflow-prometheus"
RAY_START_CMD = "ray start --head --dashboard-host=0.0.0.0 --metrics-export-port=9812"
PROM_CONFIG_TEMPLATE = """
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
- job_name: 'ray'
  static_configs:
    - targets: ['{host}:9812']
"""


def _port_is_open(port: str, host: str = "http://localhost", timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except Exception:
        return False
    else:
        sock.close()
        return True


def local_runtime_is_initialized():
    for port in ["8265", "9090"]:
        if not _port_is_open(port):
            return False
    return True


def start_prometheus() -> str:
    prom_config = tempfile.mktemp(suffix=".yaml")
    container_name = f"{LAUNCHFLOW_PROM_CONTAINER_NAME}-{random.randint(0, 1000)}"
    if platform.system().lower() == "darwin":
        with open(prom_config, "w") as f:
            f.write(PROM_CONFIG_TEMPLATE.format(host="host.docker.internal"))
        cmd = f"docker run -p 9090:9090 -v {prom_config}:/etc/prometheus/prometheus.yml -d --name {container_name} prom/prometheus"  # noqa: E501
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            host = s.getsockname()[0]
        except Exception:
            host = "host.docker.internal"
        finally:
            s.close()
        with open(prom_config, "w") as f:
            f.write(PROM_CONFIG_TEMPLATE.format(host=host))
        cmd = f"docker run -p 9090:9090 --add-host host.docker.internal:host-gateway -v {prom_config}:/etc/prometheus/prometheus.yml -d --name {container_name} prom/prometheus"  # noqa: E501
    subprocess.run(cmd, shell=True)
    return container_name


def stop_prometheus(container_name: str) -> str:
    subprocess.run(f"docker stop {container_name}", shell=True)
    subprocess.run(f"docker rm {container_name}", shell=True)


def start_ray() -> str:
    subprocess.check_call("ray start --head --metrics-export-port=9812", shell=True)


def stop_ray():
    subprocess.run("ray stop", shell=True)


def initialize_local_runtime_environment_and_block():
    start_ray()
    container_name = start_prometheus()

    atexit.register(functools.partial(stop_prometheus, container_name))
    atexit.register(stop_ray)
    while True:
        # Loop here to keep the process open. Then when the user kills it we shut
        # everything down.
        pass


def initialize_local_runtime_environment():
    start_ray()
    start_prometheus()


def shutdown_local_runtime_environment():
    subprocess.run("ray stop", shell=True)
    subprocess.run("fuser -k 9090/tcp", shell=True)


async def stream_deployment_logs_async(
    deployment_id: str, cluster_address: str = RAY_CLUSTER_ADDRESS
):
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(
            f"{cluster_address}/api/jobs/{deployment_id}/logs/tail"
        )

        while True:
            msg = await ws.receive()

            if msg.type == aiohttp.WSMsgType.TEXT:
                print(msg.data, end="")
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                pass


def stream_deployment_logs(
    deployment_id: str, cluster_address: str = RAY_CLUSTER_ADDRESS
):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        stream_deployment_logs_async(deployment_id, cluster_address)
    )
    loop.close()


def get_deployment_info(deployment_id: str):
    resp = requests.get(f"http://127.0.0.1:8265/api/jobs/{deployment_id}")
    ray_info = json.loads(resp.text)
    deployment_info = {
        "id": ray_info["submission_id"],
        "runtime": "LOCAL",
        "deployment_status": ray_info["status"],
        "latest_metrics": {
            "total_throughput": "0",
            "avg_throughput": "0",
            "processor_latency": "0",
            "batch_latency": "0",
            "total_latency": "0",
            "num_concurrency": "0",
            "avg_buffer_size": "0",
            "num_replicas": "0",
            "backlog": "0",
        },
    }
    if ray_info["status"] in ["RUNNING", "PENDING"]:
        deployment_info["latest_metrics"] = {
            "total_throughput": queries.total_throughput(ray_info["job_id"]),
            "avg_throughput": queries.avg_throughput(ray_info["job_id"]),
            "processor_latency": queries.processor_latency(ray_info["job_id"]),
            "batch_latency": queries.batch_latency(ray_info["job_id"]),
            "total_latency": queries.total_latency(ray_info["job_id"]),
            "num_concurrency": queries.num_concurrency(ray_info["job_id"]),
            "avg_buffer_size": queries.avg_buffer_size(ray_info["job_id"]),
            "num_replicas": queries.num_replicas(ray_info["job_id"]),
            "backlog": queries.backlog(ray_info["job_id"]),
        }
    return deployment_info


def ping_deployment_info(
    deployment_ids: List[str],
    extension_server_address: Optional[str] = None,
    cluster_address: str = RAY_CLUSTER_ADDRESS,
):
    print(f"pinging deployment status for {len(deployment_ids)} deployments...")
    for deployment_id in deployment_ids:
        deployment_info = get_deployment_info(deployment_id)
        print(deployment_info)
        if extension_server_address is not None:
            requests.post(extension_server_address, json=deployment_info)


async def stream_deployment_info_async(
    deployment_id: str,
    extension_server_address: Optional[str] = None,
    cluster_address: str = RAY_CLUSTER_ADDRESS,
):
    print("streaming deployment status...")
    while True:
        deployment_info = get_deployment_info(deployment_id)
        if extension_server_address is not None:
            requests.post(extension_server_address, json=deployment_info)
        if deployment_info["deployment_status"] in ["FAILED", "STOPPED", "SUCCEEDED"]:
            break
        await asyncio.sleep(3)


def stream_deployment_info(
    deployment_id: str,
    extension_server_address: Optional[str] = None,
    cluster_address: str = RAY_CLUSTER_ADDRESS,
):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        stream_deployment_info_async(
            deployment_id, extension_server_address, cluster_address
        )
    )
    loop.close()
