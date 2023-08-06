"""Functions for executing command in AWS ECS Tasks."""
from typing import TYPE_CHECKING

from boto3 import Session

if TYPE_CHECKING:
    from mypy_boto3_ecs import ECSClient


def get_aws_profile_choices(*, session: Session) -> list[tuple[str, str]]:
    """Return a list of aws profile choices."""
    profile = session.profile_name
    profile_choices = session.available_profiles
    profile_choices.sort()
    try:
        profile_choices.insert(0, profile_choices.pop(profile_choices.index(profile)))
    except ValueError:
        profile_choices.insert(0, profile)
    return [(value, value) for value in profile_choices]


def is_cluster_valid(cluster: str, *, ecs_client: "ECSClient") -> bool:
    """Return whether the cluster is valid."""
    return bool(ecs_client.describe_clusters(clusters=[cluster])["clusters"])


def get_cluster_choices(*, ecs_client: "ECSClient") -> list[tuple[str, str]]:
    """Return a list of cluster choices."""
    cluster_arns = ecs_client.list_clusters()["clusterArns"]
    cluster_choices = [
        cluster["clusterName"]
        for cluster in ecs_client.describe_clusters(clusters=cluster_arns)["clusters"]
    ]
    cluster_choices.sort()
    return [(value, value) for value in cluster_choices]


def is_service_name_valid(
    service_name: str, *, cluster: str, ecs_client: "ECSClient"
) -> bool:
    """Return whether the service name is valid."""
    return bool(
        ecs_client.describe_services(cluster=cluster, services=[service_name])[
            "services"
        ]
    )


def get_service_name_choices(
    *, cluster: str, ecs_client: "ECSClient"
) -> list[tuple[str, str]]:
    """Return a list of service name choices for the given cluster."""
    service_arns = ecs_client.list_services(cluster=cluster)["serviceArns"]
    service_choices = [
        service["serviceName"]
        for service in ecs_client.describe_services(
            cluster=cluster, services=service_arns
        )["services"]
    ]
    service_choices.sort()
    return [(value, value) for value in service_choices]


def get_task_choices(
    *, cluster: str, service_name: str, ecs_client: "ECSClient"
) -> list[tuple[str, str]]:
    """Return a list of task choices for the given cluster."""
    task_choices = ecs_client.list_tasks(cluster=cluster, serviceName=service_name)[
        "taskArns"
    ]
    task_choices.sort()
    return [(value, value) for value in task_choices]
