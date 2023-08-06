🔖 [Table of Contents](../../README.md) / [Concepts](../README.md)

# Task

Zrb supports the following tasks:

- [Python task](./python-task.md)
- [Cmd task](./cmd-task.md)
- [Docker-Compose task](./docker-compose-task.md)
- [HTTP checker](./http-checker.md)
- [Port checker](./port-checker.md)
- [Path checker](./path-checker.md)
- [Resource maker](./resource-maker.md)

Every task has its inputs, environments, and upstreams. By defining the upstreams, you can make several tasks run in parallel. Let's see the following example:

```
install-pip --------------------------------------> run-server
                                             |
install-node-modules  ---> build-frontend ----
```

```python
# File location: zrb_init.py
from zrb import CmdTask, HttpChecker, EnvFile, runner

# Install pip package for requirements.txt in src directory
install_pip_packages = CmdTask(
    name='install-pip',
    cmd='pip install -r requirements.txt',
    cwd='src'
)

# Install node modules in src/frontend directory
install_node_modules = CmdTask(
    name='install-node-modules',
    cmd='npm install --save-dev',
    cwd='src/frontend'
)

# Build src/frontend
# To build the frontend, you need to make sure that node_modules has already been installed.
build_frontend = CmdTask(
    name='build-frontend',
    cmd='npm run build',
    cwd='src/frontend',
    upstreams=[install_node_modules]
)

# Start the server.
# In order to start the server, you need to make sure that:
# - Necessary pip packages has been already installed
# - Frontend has already been built
# By default it should use environment defined in `src/template.env`.
# You can set the port using environment variable WEB_PORT
# This WEB_PORT environment will be translated into PORT variable internally
# You can use the port to check whether a server is ready or not.
run_server = CmdTask(
    name='run-server',
    envs=[
        Env(name='PORT', os_name='WEB_PORT', default='3000')
    ],
    env_files=[
        EnvFile(env_file='src/template.env', prefix='WEB')
    ]
    cmd='python main.py',
    cwd='src',
    upstreams=[
        install_pip_packages,
        build_frontend
    ],
    checkers=[HTTPChecker(port='{{env.PORT}}')],
)
runner.register(run_server)
```

Once defined, you can start the server by invoking the following command:

```bash
zrb run-server
```

Zrb will make sure that the tasks are executed in order based on their upstreams.
You will also see that `install-pip-packages` and `install-node-modules` are executed in parallel since they are independent of each other.

🔖 [Table of Contents](../../README.md) / [Concepts](../README.md)
