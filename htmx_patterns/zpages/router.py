from datetime import datetime, timezone
from kubernetes import client, config as kubernetes_config
from kubernetes.config.config_exception import ConfigException
import os
from pydantic import BaseModel

from fastapi import APIRouter

from htmx_patterns.config import get_config
from typing import Union

zpages_router = APIRouter(tags=["zpages"])

config = get_config()


def format_uptime(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, min = divmod(minutes, 60)
    days, hr = divmod(hours, 24)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hr:
        parts.append(f"{hr}h")
    if min:
        parts.append(f"{min}m")
    parts.append(f"{sec}s")

    return " ".join(parts)


class PodInfo(BaseModel):
    pod_name: str
    namespace: str
    node_name: str
    container_image: str
    start_time: Union[str, datetime]
    pod_uptime: Union[str, int]


class Ready(BaseModel):
    ready: bool
    timestamp: str
    app_version: str

    pod_info: PodInfo


def get_pod_info():
    pod_name = os.getenv("KUBERNETES_POD_NAME")
    namespace = os.getenv("KUBERNETES_POD_NAMESPACE")

    try:
        kubernetes_config.load_incluster_config()
    except ConfigException:
        return PodInfo(
            pod_name="unknown",
            namespace="unknown",
            node_name="unknown",
            pod_ip="unknown",
            container_image="unknown",
            start_time="unknown",
            pod_uptime="unknown",
        )
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    start_time = pod.status.start_time
    now = datetime.now(timezone.utc)
    uptime_seconds = int((now - start_time).total_seconds())

    return PodInfo(
        pod_name=pod.metadata.name,
        namespace=pod.metadata.namespace,
        node_name=pod.spec.node_name,
        container_image=pod.spec.containers[0].image,
        start_time=pod.status.start_time,
        pod_uptime=format_uptime(uptime_seconds),
    )


@zpages_router.get("/readyz")
async def root() -> Ready:
    pod_info = get_pod_info()
    ready = Ready(
        ready=True,
        timestamp=datetime.now(timezone.utc).isoformat(),
        app_version=config.app_version,
        pod_info=pod_info,
    )
    return ready
