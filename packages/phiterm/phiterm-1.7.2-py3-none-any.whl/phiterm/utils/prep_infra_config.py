from typing import Optional, List

from phidata.infra.config import InfraConfig
from phidata.workspace.config import WorkspaceConfig
from phidata.workspace.settings import WorkspaceSettings

from phiterm.utils.log import logger
from phiterm.workspace.ws_enums import WorkspaceConfigType


def prep_infra_config(
    infra_config: InfraConfig,
    ws_config: WorkspaceConfig,
) -> InfraConfig:
    logger.debug(f"Updating {infra_config.__class__.__name__} using WorkspaceConfig")

    ######################################################################
    # NOTE: VERY IMPORTANT TO GET RIGHT
    # Prep InfraConfig using the WorkspaceConfig
    # 1. Pass down the paths from the WorkspaceConfig
    #       These paths are used everywhere from Infra, Apps, Resources, Workflows
    # 2. Pass down local_env, docker_env, k8s_env
    # 3. Pass down common cloud configuration. eg: aws_region, aws_profile
    ######################################################################

    # -*- Path parameters
    infra_config.scripts_dir = ws_config.scripts_dir
    infra_config.storage_dir = ws_config.storage_dir
    infra_config.meta_dir = ws_config.meta_dir
    infra_config.products_dir = ws_config.products_dir
    infra_config.notebooks_dir = ws_config.notebooks_dir
    infra_config.workflows_dir = ws_config.workflows_dir
    # The workspace_root_path is the ROOT directory for the workspace
    infra_config.workspace_root_path = ws_config.workspace_root_path
    infra_config.workspace_config_dir = ws_config.workspace_config_dir
    infra_config.workspace_config_file_path = ws_config.workspace_config_file_path

    # -*- Environment parameters
    # only update the param if they are not available.
    # i.e. prefer the configs param if provided
    if infra_config.local_env is None and ws_config.local_env is not None:
        infra_config.local_env = ws_config.local_env
    if infra_config.local_env_file is None and ws_config.local_env_file is not None:
        infra_config.local_env_file = ws_config.local_env_file
    if infra_config.docker_env is None and ws_config.docker_env is not None:
        infra_config.docker_env = ws_config.docker_env
    if infra_config.docker_env_file is None and ws_config.docker_env_file is not None:
        infra_config.docker_env_file = ws_config.docker_env_file
    if infra_config.k8s_env is None and ws_config.k8s_env is not None:
        infra_config.k8s_env = ws_config.k8s_env
    if infra_config.k8s_env_file is None and ws_config.k8s_env_file is not None:
        infra_config.k8s_env_file = ws_config.k8s_env_file

    ws_settings: Optional[WorkspaceSettings] = ws_config.ws_settings
    if ws_settings is not None:
        # -*- AWS parameters
        # only update the param if they are available.
        # i.e. prefer the configs param if provided
        if infra_config.aws_region is None and ws_settings.aws_region is not None:
            infra_config.aws_region = ws_settings.aws_region
        if infra_config.aws_profile is None and ws_settings.aws_profile is not None:
            infra_config.aws_profile = ws_settings.aws_profile
        if (
            infra_config.aws_config_file is None
            and ws_settings.aws_config_file is not None
        ):
            infra_config.aws_config_file = ws_settings.aws_config_file
        if (
            infra_config.aws_shared_credentials_file is None
            and ws_settings.aws_shared_credentials_file is not None
        ):
            infra_config.aws_shared_credentials_file = (
                ws_settings.aws_shared_credentials_file
            )

        # -*- `phi` cli parameters
        # only update the param if they are available.
        # i.e. prefer the configs param if provided
        if (
            infra_config.continue_on_create_failure is None
            and ws_settings.continue_on_create_failure is not None
        ):
            infra_config.continue_on_create_failure = (
                ws_settings.continue_on_create_failure
            )
        if (
            infra_config.continue_on_delete_failure is None
            and ws_settings.continue_on_delete_failure is not None
        ):
            infra_config.continue_on_delete_failure = (
                ws_settings.continue_on_delete_failure
            )
        if (
            infra_config.continue_on_patch_failure is None
            and ws_settings.continue_on_patch_failure is not None
        ):
            infra_config.continue_on_patch_failure = (
                ws_settings.continue_on_patch_failure
            )

    return infra_config


def filter_and_prep_configs(
    ws_config: WorkspaceConfig,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    order: Optional[str] = "create",
) -> List[InfraConfig]:
    # Step 1. Filter configs
    # 1.1: Filter by config type: docker/k8s/aws
    filtered_configs: List[InfraConfig] = []
    if target_config is None:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        if order == "delete":
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
        else:
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
    elif target_config == WorkspaceConfigType.docker:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        else:
            logger.error("No DockerConfig provided")
    elif target_config == WorkspaceConfigType.k8s:
        if ws_config.k8s is not None:
            filtered_configs.extend(ws_config.k8s)
        else:
            logger.error("No K8sConfig provided")
    elif target_config == WorkspaceConfigType.aws:
        if ws_config.aws is not None:
            filtered_configs.extend(ws_config.aws)
        else:
            logger.error("No AwsConfig provided")

    # 1.2: Filter by env: dev/stg/prd
    configs_after_env_filter: List[InfraConfig] = []
    if target_env is None or target_env == "all":
        configs_after_env_filter = filtered_configs
    else:
        for config in filtered_configs:
            if config.env is None:
                continue
            if target_env == config.env:
                configs_after_env_filter.append(config)
    # logger.debug("Filtered configs: {}`".format(configs_after_env_filter))

    # Step 2. Prepare configs
    ready_to_use_configs: List[InfraConfig] = []
    for config in configs_after_env_filter:
        if not isinstance(config, InfraConfig):
            logger.error(f"{config} is not an instance of InfraConfig")
            continue
        if not config.is_valid():
            logger.warning(f"Skipping {config.__class__}\n")
            continue
        if not config.enabled:
            logger.debug(
                f"{config.__class__.__name__} for env {config.__class__.env} disabled"
            )
            continue

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        ######################################################################

        _config = prep_infra_config(
            infra_config=config,
            ws_config=ws_config,
        )
        ready_to_use_configs.append(_config)

    # Return filtered and prepared configs
    return ready_to_use_configs
