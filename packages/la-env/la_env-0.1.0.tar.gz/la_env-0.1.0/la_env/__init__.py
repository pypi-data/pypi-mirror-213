import os


class EnvironmentMissing(Exception):
    pass


def env_exists(envs: list[str]) -> None:
    for e in envs:
        if e not in os.environ:
            raise EnvironmentMissing(f"Environment {e} not declared")
