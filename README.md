# LINDI

## Project Structure

```
.
├── conf/                    # configuration files
├── docs/                    # Project documentation
├── slurm/                   # HPC job scheduling configs
├── src/                     # Python source code
├── pyproject.toml           # Python project config
└── taskfile.yaml            # Task automation definitions
```

## Development Setup

### Installing Task

Task is a task runner/build tool that aims to be simpler and easier to use than GNU Make. You'll need to install it before you can run any of the development tasks.

```bash
brew install go-task/tap/go-task
```

### Environment

To set up the development environment, run:

```bash
task local:env
```

This command will install all necessary dependencies and configure your local development environment.

> [!NOTE]
> `task` will install `direnv` which sets required environment variables automatically. You might want to hook it into your shell by following the [setup guide](https://direnv.net/docs/hook.html). If you choose not to set up the hook, you'll need to prefix your commands with `direnv exec . <command>` to load the environment variables.
