import os
import yaml

from p360_export.exceptions.config import ConfigAttributeMissingException
from p360_export.utils.utils import get_repository_root_fs_path, merge_dicts


class SkeletonConfigGetter:
    def __init__(self):
        root_module = self.__resolve_daipe_root_module()

        self.__skeleton_config_folder = os.path.join(get_repository_root_fs_path(), f"src/{root_module}/_config/")
        self.__kernel_environment_placeholder = "%kernel.environment%"
        self.__env = os.environ.get("APP_ENV")

    def __resolve_daipe_root_module(self):
        root_module_name_search_exclude = ["daipe.py", "__pycache__"]

        filenames = os.listdir(os.path.join(get_repository_root_fs_path(), "src"))

        root_module = [filename for filename in filenames if filename not in root_module_name_search_exclude]

        if len(root_module) != 1:
            raise Exception("Cannot resolve daipe root module. There is more than one file under 'src'.")

        return root_module[0]

    def __replace_kernel_environment(self, unparsed_config: str) -> str:
        if self.__env:
            unparsed_config = unparsed_config.replace(self.__kernel_environment_placeholder, self.__env)

        return unparsed_config

    def __load_config(self, config_path: str) -> dict:
        if not os.path.exists(config_path):
            return {}

        with open(config_path, "r", encoding="utf-8") as f:
            unparsed_config = self.__replace_kernel_environment(unparsed_config=f.read())

        config = yaml.load(unparsed_config, Loader=yaml.BaseLoader)

        parameters = config.get("parameters")

        return {
            "p360_export": parameters.get("p360_export", {}),
            "featurestorebundle": parameters.get("featurestorebundle", {}),
        }

    def __get_env_specifig_config(self) -> dict:
        config_path = os.path.join(self.__skeleton_config_folder, f"config_{self.__env}.yaml")
        return self.__load_config(config_path)

    def __get_main_config(self) -> dict:
        config_path = os.path.join(self.__skeleton_config_folder, "config.yaml")
        return self.__load_config(config_path)

    def get(self) -> dict:
        main_config = self.__get_main_config()
        env_specific_config = self.__get_env_specifig_config()

        merged_config = merge_dicts(main_config, env_specific_config)

        for section in ["p360_export", "featurestorebundle"]:
            if not merged_config[section]:
                raise ConfigAttributeMissingException(f"Section {section} not defined in config")

        return merged_config
