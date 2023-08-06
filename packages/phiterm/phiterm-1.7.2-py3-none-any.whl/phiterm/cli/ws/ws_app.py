"""Phi Workspace Cli

This is the entrypoint for the `phi ws` commands
"""
from pathlib import Path
from typing import Optional, cast

import typer

from phiterm.utils.cli_console import (
    print_error,
    print_info,
    print_heading,
    print_available_workspaces,
    print_conf_not_available_msg,
    print_active_workspace_not_available,
)
from phiterm.utils.log import logger, set_log_level_to_debug
from phiterm.workspace.ws_enums import WorkspaceConfigType

ws_app = typer.Typer(
    name="ws",
    short_help="Manage workspaces",
    help="""\b
Use `phi ws <command>` to create, setup, start or stop your workspace.
Run `phi ws <command> --help` for more info.
""",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)


@ws_app.command(short_help="Create a new workspace in the current directory.")
def create(
    template: Optional[str] = typer.Option(
        None,
        "-t",
        "--template",
        help="Starter template for the workspace.",
        show_default=False,
    ),
    name: Optional[str] = typer.Option(
        None,
        "-n",
        "--name",
        help="Name of the new workspace.",
        show_default=False,
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Create a new workspace in the current directory using a starter template
    \b
    Examples:
    > phi ws create -t ai-app     -> Create an `ai-app` workspace in the current directory
    > phi ws create -t ai-app -n ai  -> Create an `ai-app` workspace named `ai` in the current directory
    """
    from phiterm.workspace.ws_operator import create_workspace

    if print_debug_log:
        set_log_level_to_debug()

    create_workspace(template=template, name=name)


@ws_app.command(short_help="Setup phidata workspace from the current directory")
def setup(
    path: Optional[str] = typer.Argument(
        None,
        help="Optional path to workspace.",
        show_default=False,
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Setup a phidata workspace. This command can be run from the workspace directory OR using the workspace path.
    \b
    Examples:
    > `phi ws setup`           -> Setup the current directory as a workspace
    > `phi ws setup ai-app`    -> Setup the `ai-app` folder as a workspace
    """
    from phiterm.workspace.ws_operator import setup_workspace

    if print_debug_log:
        set_log_level_to_debug()

    # By default, we assume this command is run from the workspace directory
    ws_root_path: Path = Path(".").resolve()

    # If the user provides a path, use that to setup the workspace
    if path is not None:
        ws_root_path = Path(".").joinpath(path).resolve()

    setup_workspace(ws_root_path=ws_root_path)


@ws_app.command(short_help="Create resources for active workspace")
def up(
    resource_filter: Optional[str] = typer.Argument(
        None,
        help="Resource filter. Format - ENV:CONFIG:GROUP:NAME:TYPE",
        metavar="[FILTER]",
    ),
    env_filter: Optional[str] = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to deploy"
    ),
    config_filter: Optional[str] = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to deploy"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deploying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Create resources for the active workspace.
    Options can be used to limit the resources to create.
      --env     : Env (dev, stg, prd)
      --group   : Group name
      --name    : Resource name
      --type    : Resource type
      --config  : Config type (docker, aws, k8s)
    \b
    Filters can also be provided as a single argument - ENV:CONFIG:GROUP:NAME:TYPE
    \b
    Examples:
    > `phi ws up`            -> Deploy all resources
    > `phi ws up dev`        -> Deploy all dev resources
    > `phi ws up prd`        -> Deploy all prd resources
    > `phi ws up prd:aws`    -> Deploy all prd aws resources
    > `phi ws up prd:::s3`    -> Deploy prd resources matching name s3
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import deploy_workspace
    from phiterm.utils.load_env import load_env
    from phiterm.utils.ws_filter import parse_ws_filter

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    current_path: Path = Path(".").resolve()
    if active_ws_data.ws_root_path != current_path and not auto_confirm:
        ws_at_current_path = phi_conf.get_ws_data_by_path(current_path)
        if ws_at_current_path is not None:
            print_info(
                f"Workspace at the current directory ({ws_at_current_path.ws_name}) is not the Active Workspace ({active_ws_data.ws_name})"
            )
            update_active_workspace = typer.confirm(
                f"Update active workspace to {ws_at_current_path.ws_name}", default=True
            )
            if update_active_workspace:
                phi_conf.active_ws_name = ws_at_current_path.ws_name
                active_ws_data = ws_at_current_path

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=active_ws_data.ws_root_path,
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_group: Optional[str] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    # derive env:config:name:type:group from ws_filter
    if resource_filter is not None:
        if not isinstance(resource_filter, str):
            raise TypeError(
                f"Invalid resource_filter. Expected: str, Received: {type(resource_filter)}"
            )
        (
            target_env,
            target_config_str,
            target_group,
            target_name,
            target_type,
        ) = parse_ws_filter(resource_filter)

    # derive env:config:name:type:group from command options
    if target_env is None and env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if (
        target_group is None
        and group_filter is not None
        and isinstance(group_filter, str)
    ):
        target_group = group_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter

    # derive env:config:name:type:group from defaults
    if target_env is None:
        target_env = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )
    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Deploying workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    print_heading("Deploying workspace: {}\n".format(active_ws_data.ws_name))
    deploy_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@ws_app.command(short_help="Delete resources for active workspace")
def down(
    resource_filter: Optional[str] = typer.Argument(
        None,
        help="Resource filter. Format - ENV:CONFIG:GROUP:NAME:TYPE",
        metavar="[FILTER]",
    ),
    env_filter: str = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to shut down"
    ),
    config_filter: str = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to shut down"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deleted and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deleting resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Delete resources for the active workspace.
    Options can be used to limit the resources to delete.
      --env     : Env (dev, stg, prd)
      --group   : Group name
      --name    : Resource name
      --type    : Resource type
      --config  : Config type (docker, aws, k8s)
    \b
    Filters can also be provided as a single argument - ENV:CONFIG:GROUP:NAME:TYPE
    \b
    Examples:
    > `phi ws down`            -> Delete all resources
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import shutdown_workspace
    from phiterm.utils.load_env import load_env
    from phiterm.utils.ws_filter import parse_ws_filter

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    current_path: Path = Path(".").resolve()
    if active_ws_data.ws_root_path != current_path and not auto_confirm:
        ws_at_current_path = phi_conf.get_ws_data_by_path(current_path)
        if ws_at_current_path is not None:
            print_info(
                f"Workspace at the current directory ({ws_at_current_path.ws_name}) is not the Active Workspace ({active_ws_data.ws_name})"
            )
            update_active_workspace = typer.confirm(
                f"Update active workspace to {ws_at_current_path.ws_name}", default=True
            )
            if update_active_workspace:
                phi_conf.active_ws_name = ws_at_current_path.ws_name
                active_ws_data = ws_at_current_path

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=active_ws_data.ws_root_path,
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_group: Optional[str] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    # derive env:config:name:type:group from ws_filter
    if resource_filter is not None:
        if not isinstance(resource_filter, str):
            raise TypeError(
                f"Invalid resource_filter. Expected: str, Received: {type(resource_filter)}"
            )
        (
            target_env,
            target_config_str,
            target_group,
            target_name,
            target_type,
        ) = parse_ws_filter(resource_filter)

    # derive env:config:name:type:group from command options
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if (
        target_group is None
        and group_filter is not None
        and isinstance(group_filter, str)
    ):
        target_group = group_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_env is None and env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter

    # derive env:config:name:type:group from defaults
    if target_env is None:
        target_env = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )
    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Shutting down workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    print_heading("Shutdown workspace: {}\n".format(active_ws_data.ws_name))
    shutdown_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@ws_app.command(short_help="Update resources for active workspace")
def patch(
    resource_filter: Optional[str] = typer.Argument(
        None,
        help="Resource filter. Format - ENV:CONFIG:GROUP:NAME:TYPE",
        metavar="[FILTER]",
    ),
    env_filter: str = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to patch"
    ),
    config_filter: str = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to patch"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be patched and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before patching resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Update resources for the active workspace.
    Options can be used to limit the resources to update.
      --env     : Env (dev, stg, prd)
      --group   : Group name
      --name    : Resource name
      --type    : Resource type
      --config  : Config type (docker, aws, k8s)
    \b
    Filters can also be provided as a single argument - ENV:CONFIG:GROUP:NAME:TYPE
    Examples:
    \b
    > `phi ws patch`           -> Patch all resources
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import patch_workspace
    from phiterm.utils.load_env import load_env
    from phiterm.utils.ws_filter import parse_ws_filter

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    current_path: Path = Path(".").resolve()
    if active_ws_data.ws_root_path != current_path and not auto_confirm:
        ws_at_current_path = phi_conf.get_ws_data_by_path(current_path)
        if ws_at_current_path is not None:
            print_info(
                f"Workspace at the current directory ({ws_at_current_path.ws_name}) is not the Active Workspace ({active_ws_data.ws_name})"
            )
            update_active_workspace = typer.confirm(
                f"Update active workspace to {ws_at_current_path.ws_name}", default=True
            )
            if update_active_workspace:
                phi_conf.active_ws_name = ws_at_current_path.ws_name
                active_ws_data = ws_at_current_path

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=active_ws_data.ws_root_path,
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_group: Optional[str] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    # derive env:config:name:type:group from ws_filter
    if resource_filter is not None:
        if not isinstance(resource_filter, str):
            raise TypeError(
                f"Invalid resource_filter. Expected: str, Received: {type(resource_filter)}"
            )
        (
            target_env,
            target_config_str,
            target_group,
            target_name,
            target_type,
        ) = parse_ws_filter(resource_filter)

    # derive env:config:name:type:group from command options
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if (
        target_group is None
        and group_filter is not None
        and isinstance(group_filter, str)
    ):
        target_group = group_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_env is None and env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter

    # derive env:config:name:type:group from defaults
    if target_env is None:
        target_env = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )
    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Patching workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    print_heading("Patching workspace: {}\n".format(active_ws_data.ws_name))
    patch_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@ws_app.command(short_help="Restart resources for active workspace")
def restart(
    resource_filter: Optional[str] = typer.Argument(
        None,
        help="Resource filter. Format - ENV:CONFIG:GROUP:NAME:TYPE",
        metavar="[FILTER]",
    ),
    env_filter: str = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to restart"
    ),
    config_filter: str = typer.Option(
        None, "-i", "--config", metavar="", help="Filter the config to restart"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be restarted and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before restarting resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Restarts the active workspace. i.e. runs `phi ws down` and then `phi ws up`.

    \b
    Examples:
    > `phi ws restart`
    """
    from time import sleep

    down(
        resource_filter=resource_filter,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        group_filter=group_filter,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
        print_debug_log=print_debug_log,
        force=force,
    )
    print_info("Sleeping for 2 seconds..")
    sleep(2)
    up(
        resource_filter=resource_filter,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        group_filter=group_filter,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
        print_debug_log=print_debug_log,
        force=force,
    )


@ws_app.command(short_help="Show status for workspace resources")
def status(
    resource_filter: Optional[str] = typer.Argument(
        None,
        help="Resource filter. Format - ENV:CONFIG:GROUP:NAME:TYPE",
        metavar="[FILTER]",
    ),
    env_filter: str = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment"
    ),
    config_filter: str = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be displayed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before displaying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Get resource status for active workspace.
    Options can be used to limit the resources to update.
      --env     : Env (dev, stg, prd)
      --group   : Group name
      --name    : Resource name
      --type    : Resource type
      --config  : Config type (docker, aws, k8s)
    \b
    Filters can also be provided as a single argument - ENV:CONFIG:GROUP:NAME:TYPE
    Examples:
    \b
    > `phi ws status`           -> Show status for all resources
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import print_workspace_status
    from phiterm.utils.load_env import load_env
    from phiterm.utils.ws_filter import parse_ws_filter

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    current_path: Path = Path(".").resolve()
    if active_ws_data.ws_root_path != current_path and not auto_confirm:
        ws_at_current_path = phi_conf.get_ws_data_by_path(current_path)
        if ws_at_current_path is not None:
            print_info(
                f"Workspace at the current directory ({ws_at_current_path.ws_name}) is not the Active Workspace ({active_ws_data.ws_name})"
            )
            update_active_workspace = typer.confirm(
                f"Update active workspace to {ws_at_current_path.ws_name}", default=True
            )
            if update_active_workspace:
                phi_conf.active_ws_name = ws_at_current_path.ws_name
                active_ws_data = ws_at_current_path

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=active_ws_data.ws_root_path,
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_group: Optional[str] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    # derive env:config:name:type:group from ws_filter
    if resource_filter is not None:
        if not isinstance(resource_filter, str):
            raise TypeError(
                f"Invalid resource_filter. Expected: str, Received: {type(resource_filter)}"
            )
        (
            target_env,
            target_config_str,
            target_group,
            target_name,
            target_type,
        ) = parse_ws_filter(resource_filter)

    # derive env:config:name:type:group from command options
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if (
        target_group is None
        and group_filter is not None
        and isinstance(group_filter, str)
    ):
        target_group = group_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_env is None and env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter

    # derive env/config/name/type from defaults
    if target_env is None:
        target_env = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )
    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Reading workspace status")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    print_heading("Reading workspace status: {}\n".format(active_ws_data.ws_name))
    print_workspace_status(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@ws_app.command(short_help="Prints active workspace config", hidden=True)
def config(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Prints the active workspace config

    \b
    Examples:
    $ `phi ws config`         -> Print the active workspace config
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.utils.load_env import load_env

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    # Load environment from .env
    load_env(
        dotenv_dir=active_ws_data.ws_root_path,
    )
    active_ws_data.print_to_cli()


@ws_app.command(short_help="Delete workspace from phidata", hidden=True)
def delete(
    ws_name: str = typer.Option(None, "-ws", help="Name of the workspace to delete"),
    all_workspaces: bool = typer.Option(
        False,
        "-a",
        "--all",
        help="Delete all workspaces from phidata",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Deletes the workspace record from phidata.
    NOTE: Does not delete any physical files.

    \b
    Examples:
    $ `phi ws delete`         -> Delete the active workspace from phidata
    $ `phi ws delete -a`      -> Delete all workspaces from phidata
    """
    from phiterm.conf.phi_conf import PhiConf
    from phiterm.workspace.ws_operator import delete_workspace

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    ws_to_delete = []
    # By default, we assume this command is run from the workspace directory
    if ws_name is not None:
        ws_to_delete.append(ws_name)
    else:
        if all_workspaces:
            ws_to_delete = [ws.ws_name for ws in phi_conf.available_ws]
        else:
            if phi_conf.active_ws_name is not None:
                ws_to_delete.append(phi_conf.active_ws_name)

    delete_workspace(ws_to_delete, phi_conf)


# @ws_app.command(short_help="Show steps to setup a git repo for the ws")
# def git(
#     ws_name: str = typer.Option(None, "-ws", help="[Optional] Name for the workspace"),
#     print_debug_log: bool = typer.Option(
#         False,
#         "-d",
#         "--debug",
#         help="Print debug logs.",
#     ),
# ):
#     """
#     Print steps to setup a remote git repo for the active workspace.
#
#     \b
#     Examples:
#     $ `phi ws git`
#     $ `phi ws git -ws data`
#     """
#     from pathlib import Path
#     from phiterm.enums.user_enums import VersionControlProviderEnum
#     from phiterm.workspace.ws_operator import print_git_setup
#
#     from phiterm.conf.phi_conf import PhiConf
#
#     phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not phi_conf:
#         print_conf_not_available_msg()
#         return
#
#     _ws_name: Optional[str] = None
#     ws_root_path: Optional[Path] = None
#     if ws_name:
#         _ws_name = ws_name
#         ws_root_path = phi_conf.get_ws_root_path_by_name(_ws_name)
#     else:
#         # print steps for the active workspace
#         _ws_name = phi_conf.active_ws_name
#         if _ws_name is None:
#             print_info(
#                 "Primary workspace not available, searching current directory for a workspace"
#             )
#             ws_root_path = Path(".").resolve()
#             _ws_name = phi_conf.get_ws_name_by_path(ws_root_path)
#         else:
#             ws_data = phi_conf.get_ws_data_by_name(_ws_name)
#             if ws_data is not None and ws_data.ws_root_path is not None:
#                 ws_root_path = ws_data.ws_root_path
#
#     if _ws_name is None or ws_root_path is None:
#         print_error(f"Could not find workspace at {ws_root_path}")
#         avl_ws = phi_conf.available_ws
#         if avl_ws:
#             print_available_workspaces(avl_ws)
#         return
#
#     version_control_provider = (
#         phi_conf.user.version_control_provider
#         if phi_conf.user and phi_conf.user.version_control_provider
#         else VersionControlProviderEnum.GITHUB
#     )
#     print_git_setup(
#         ws_name=_ws_name,
#         ws_root_path=ws_root_path,
#         version_control_provider=version_control_provider,
#     )
