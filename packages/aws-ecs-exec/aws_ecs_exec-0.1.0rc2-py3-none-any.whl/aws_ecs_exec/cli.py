"""Functions for executing command in AWS ECS Tasks."""
import argparse
import logging
import os
import shlex
from functools import partial
from typing import Callable

import boto3
from botocore.exceptions import ProfileNotFound

from aws_ecs_exec import exceptions, utils
from aws_ecs_exec.colors import colored, get_colored_logger
from aws_ecs_exec.widgets import confirm, select

logger = get_colored_logger(name="aws_ecs_exec")


def get_user_choice(
    *,
    choice_name: str,
    chosen_value: str | None,
    validator: Callable[[str], bool],
    choice_getter: Callable[[], list[tuple[str, str]]],
    auto_select: bool,
) -> str:
    """Choose or offer user choice."""
    if chosen_value:
        if validator(chosen_value):
            logger.info("Using chosen %s: '%s'\n", choice_name, chosen_value)
            return chosen_value

        confirm_message = (
            f"Your {choice_name} '{chosen_value}' could not be found. Do you "
            f"want to choose the {choice_name} interactively?"
        )
        if not confirm(confirm_message):
            raise exceptions.UserDeclined()

    choices = choice_getter()
    if not choices:
        raise exceptions.NoChoices()

    if auto_select and len(choices) == 1:
        choice = choices[0]
        message = colored("Using (only) %s:", color="yellow") + " %s\n"
        logger.info(message, choice_name, choice[1])
        return choice[0]

    return select(f"Which {choice_name} do you want to use?", choices=choices)


def get_args() -> argparse.Namespace:
    """Return the args passed on the cli."""
    parser = argparse.ArgumentParser(
        prog="aws_ecs_exec",
        description="Interactively choose which ECS task to connect to",
    )
    parser.add_argument(
        "-a", "--aws-profile", help="The aws profile to use", required=False
    )
    parser.add_argument(
        "-c", "--cluster", help="The cluster name or arn", required=False
    )
    parser.add_argument("-s", "--service-name", help="The service name", required=False)
    parser.add_argument(
        "-C",
        "--command",
        help="The command to execute in the container (default: /bin/bash)",
        default="/bin/bash",
    )
    parser.add_argument(
        "--auto-select",
        help="Whether to automatically select values when there is a single choice",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "-e",
        "--extra-args",
        help=(
            "Extra arguments that will be passed to the aws cli command "
            "(can be supplied multiple times)"
        ),
        action="append",
    )
    parser.add_argument(
        "--colors",
        help="Whether to colorise output",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Log debug statements (default: False)",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def execute_command(
    *,
    aws_profile: str,
    cluster: str,
    task_arn: str,
    command: str,
    extra_args: list[str],
) -> None:
    """Execute the command."""
    # replace this process with the aws cli command
    path = "/usr/bin/env"
    arguments = [
        "aws",
        "--profile",
        aws_profile,
        "ecs",
        "execute-command",
        "--cluster",
        cluster,
        "--task",
        task_arn,
        "--command",
        command,
        "--interactive",
    ] + extra_args

    logger.debug("Running command: %s\n", shlex.join([path] + arguments))

    os.execv(path, ["env"] + arguments)


def get_extra_args(extra_args: list[str] | None) -> list[str]:
    """Return extra_args as list of strings split by shlex."""
    if not extra_args:
        return []
    return [split_arg for arg in extra_args for split_arg in shlex.split(arg)]


# pylint: disable-next=too-many-return-statements
def entrypoint():
    """Execute a command in an AWS ECS Task."""
    try:
        args = get_args()

        if args.verbose:
            logger.setLevel(logging.DEBUG)

        if args.colors is not None:
            if args.colors:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = "true"

        try:
            aws_profile = get_user_choice(
                choice_name="aws profile",
                chosen_value=args.aws_profile,
                validator=lambda _: True,
                choice_getter=partial(
                    utils.get_aws_profile_choices, session=boto3.Session()
                ),
                auto_select=args.auto_select,
            )
            session = boto3.Session(profile_name=aws_profile)
        except exceptions.NoChoices:
            logger.error("You have no aws profiles configured.")
            return 1
        except ProfileNotFound:
            logger.error("Could not find aws profile '%s'", aws_profile)
            return 1

        try:
            session = boto3.Session(profile_name=aws_profile)
        except ProfileNotFound:
            logger.error("Could not find aws profile '%s'", aws_profile)
            return 1

        ecs_client = session.client("ecs")

        try:
            cluster = get_user_choice(
                choice_name="cluster",
                chosen_value=args.cluster,
                validator=partial(utils.is_cluster_valid, ecs_client=ecs_client),
                choice_getter=partial(utils.get_cluster_choices, ecs_client=ecs_client),
                auto_select=args.auto_select,
            )
        except exceptions.NoChoices:
            logger.error("There are no clusters for this account")
            return 1

        try:
            service_name = get_user_choice(
                choice_name="service name",
                chosen_value=args.service_name,
                validator=partial(
                    utils.is_service_name_valid, cluster=cluster, ecs_client=ecs_client
                ),
                choice_getter=partial(
                    utils.get_service_name_choices,
                    cluster=cluster,
                    ecs_client=ecs_client,
                ),
                auto_select=args.auto_select,
            )
        except exceptions.NoChoices:
            logger.error("There are no services for this cluster")
            return 1

        try:
            task_arn = get_user_choice(
                choice_name="task arn",
                chosen_value=None,
                validator=lambda _: False,
                choice_getter=partial(
                    utils.get_task_choices,
                    cluster=cluster,
                    service_name=service_name,
                    ecs_client=ecs_client,
                ),
                auto_select=args.auto_select,
            )
        except exceptions.NoChoices:
            logger.error("There are no tasks for this service")
            return 1

        return execute_command(
            aws_profile=aws_profile,
            cluster=cluster,
            task_arn=task_arn,
            command=args.command,
            extra_args=get_extra_args(args.extra_args),
        )
    except exceptions.UserDeclined:
        return 1
