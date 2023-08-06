from zrb import DockerComposeTask, runner
from zrb.builtin._group import project_group
from ._common import (
    RESOURCE_DIR, SKIP_CONTAINER_EXECUTION,
    app_container_checker, rabbitmq_checker, rabbitmq_management_checker,
    redpanda_console_checker, kafka_outside_checker,
    kafka_plaintext_checker, pandaproxy_outside_checker,
    pandaproxy_plaintext_checker,
    local_input, mode_input, host_input, https_input, image_input,
    app_env_file, compose_env_file, image_env
)
from .image import build_snake_app_name_image

compose_env_prefix = 'CONTAINER_ENV_PREFIX'
all_compose_profiles = 'monolith,microservices,kafka,rabbitmq'
start_broker_compose_profile = '{{env.get("APP_BROKER_TYPE", "rabbitmq")}}'
start_mode_compose_profile = '{{input.get("snake_app_name_mode", "monolith")}}'
start_compose_profiles = ','.join([
    start_broker_compose_profile, start_mode_compose_profile
])

###############################################################################
# Task Definitions
###############################################################################

remove_snake_app_name_container = DockerComposeTask(
    icon='💨',
    name='remove-kebab-app-name-container',
    description='Rumove human readable app name container',
    group=project_group,
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={all_compose_profiles}',
    compose_cmd='down',
    compose_env_prefix=compose_env_prefix,
    env_files=[
        app_env_file,
        compose_env_file
    ],
    envs=[image_env]
)
runner.register(remove_snake_app_name_container)

start_snake_app_name_container = DockerComposeTask(
    icon='🐳',
    name='start-kebab-app-name-container',
    description='Start human readable app name container',
    group=project_group,
    inputs=[
        local_input,
        mode_input,
        host_input,
        https_input,
        image_input,
    ],
    skip_execution=SKIP_CONTAINER_EXECUTION,
    upstreams=[
        build_snake_app_name_image,
        remove_snake_app_name_container
    ],
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={start_compose_profiles}',
    compose_cmd='up',
    compose_env_prefix=compose_env_prefix,
    env_files=[
        app_env_file,
        compose_env_file
    ],
    envs=[image_env],
    checkers=[
        app_container_checker,
        rabbitmq_checker,
        rabbitmq_management_checker,
        kafka_outside_checker,
        kafka_plaintext_checker,
        redpanda_console_checker,
        pandaproxy_outside_checker,
        pandaproxy_plaintext_checker,
    ]
)
runner.register(start_snake_app_name_container)

stop_snake_app_name_container = DockerComposeTask(
    icon='⛔',
    name='stop-kebab-app-name-container',
    description='Stop human readable app name container',
    group=project_group,
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={all_compose_profiles}',
    compose_cmd='stop',
    compose_env_prefix=compose_env_prefix,
    env_files=[
        app_env_file,
        compose_env_file
    ],
    envs=[image_env]
)
runner.register(stop_snake_app_name_container)
