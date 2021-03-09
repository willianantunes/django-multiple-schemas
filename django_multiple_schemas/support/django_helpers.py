import os

from distutils.util import strtobool


def eval_env_as_boolean(varname, standard_value) -> bool:
    return bool(strtobool(os.getenv(varname, str(standard_value))))
