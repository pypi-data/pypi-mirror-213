from typing import Any, Optional

import requests


def _run_query(query: str) -> Optional[Any]:
    # We're pretty wide with this catch cause we don't want our check-ins to
    # fail.
    try:
        response = requests.get(
            "http://localhost:9090/api/v1/query", params={"query": query}
        ).json()
        result = response.get("data").get("result")
        return result[0].get("value")[1]
    except Exception:
        return "N/A"


def total_throughput(ray_job_id: str):
    return _run_query(
        f'sum(rate(ray_num_events_processed{{JobId="{ray_job_id}"}}[1m]))'
    )


def avg_throughput(ray_job_id: str):
    return _run_query(
        f'avg(rate(ray_num_events_processed{{JobId="{ray_job_id}"}}[1m]))'
    )


def backlog(ray_job_id: str):
    return _run_query(f'rate(ray_current_backlog{{JobId="{ray_job_id}"}}[1m])')


def num_replicas(ray_job_id: str):
    return _run_query(f'ray_num_replicas{{JobId="{ray_job_id}"}}')


def processor_latency(ray_job_id: str):
    return _run_query(f'avg_over_time(ray_process_time{{JobId="{ray_job_id}"}}[1m])')


def batch_latency(ray_job_id: str):
    return _run_query(f'avg_over_time(ray_batch_time{{JobId="{ray_job_id}"}}[1m])')


def total_latency(ray_job_id: str):
    return _run_query(f'avg_over_time(ray_total_time{{JobId="{ray_job_id}"}}[1m])')


def num_concurrency(ray_job_id: str):
    return _run_query(f'avg_over_time(ray_ppp_concurrency{{JobId="{ray_job_id}"}}[1m])')


def avg_buffer_size(ray_job_id: str):
    # return _run_query(f'avg_over_time(ray_ppp_buffer_size{{JobId="{ray_job_id}"}}[1m])')
    return "TODO"
