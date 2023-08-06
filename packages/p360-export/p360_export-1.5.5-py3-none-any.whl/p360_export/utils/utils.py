import sys
import IPython


def get_repository_root_fs_path() -> str:
    return min((path for path in sys.path if path.startswith("/Workspace/Repos")), key=len)


def resolve_dbutils():
    ipython = IPython.get_ipython()

    if not hasattr(ipython, "user_ns") or "dbutils" not in ipython.user_ns:  # type: ignore
        raise Exception("dbutils cannot be resolved")

    return ipython.user_ns["dbutils"]  # type: ignore


def merge_dicts(dict_a: dict, dict_b: dict) -> dict:
    for key in dict_b:
        if isinstance(dict_a.get(key), dict) and isinstance(dict_b.get(key), dict):
            merge_dicts(dict_a[key], dict_b[key])
        else:
            dict_a[key] = dict_b[key]

    return dict_a
