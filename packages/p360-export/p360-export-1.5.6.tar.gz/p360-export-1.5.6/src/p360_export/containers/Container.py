import yaml
import json
from os.path import dirname, abspath, join

from typing import Any, Dict, Union

from dependency_injector import containers, providers

from p360_export.ExportManager import ExportManager
from p360_export.config.SkeletonConfigGetter import SkeletonConfigGetter
from p360_export.containers.Core import Core
from p360_export.containers.DataPlatformContainer import DataPlatformContainer
from p360_export.containers.FacebookContainer import FacebookContainer
from p360_export.containers.GoogleAdsContainer import GoogleAdsContainer
from p360_export.containers.GoogleAnalytics4Container import GoogleAnalytics4Container
from p360_export.containers.SFMCContainer import SFMCContainer
from p360_export.exceptions.config import InvalidConfigException


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    skeleton_config_getter = providers.Singleton(SkeletonConfigGetter)

    core = providers.Container(Core, config=config)

    dataplatform = providers.Container(DataPlatformContainer, config=config, core=core)
    facebook = providers.Container(FacebookContainer, config=config, core=core)
    sfmc = providers.Container(SFMCContainer, config=config, core=core)
    google_ads = providers.Container(GoogleAdsContainer, config=config, core=core)
    google_analytics_4 = providers.Container(GoogleAnalytics4Container, config=config, core=core)

    manager = providers.Singleton(ExportManager, container=__self__)


def get_local_config():
    local_config_path = join(dirname(dirname(abspath(__file__))), "_config", "config.yaml")

    with open(local_config_path, "r", encoding="utf-8") as stream:
        local_config = yaml.safe_load(stream)
        return local_config["parameters"]


def set_skeleton_config(container):
    skeleton_config = container.skeleton_config_getter().get()
    container.config.from_dict(skeleton_config)


def parse_export_config(export_config: Union[str, Dict[str, Any]]) -> dict:
    if isinstance(export_config, str):
        try:
            export_config = json.loads(export_config)
        except Exception as e:
            raise InvalidConfigException("Provided config is invalid, it has to be a valid dictionary or a json") from e

    return export_config


def init_container(export_config: Union[str, Dict[str, Any]]) -> Container:
    container = Container()

    container.config.from_dict(get_local_config())
    container.config.from_dict(parse_export_config(export_config))

    container.wire(modules=[__name__])

    return container
