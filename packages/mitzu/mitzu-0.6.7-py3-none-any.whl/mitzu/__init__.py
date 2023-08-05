from mitzu.model import (
    Connection,
    ConnectionType,
    DiscoveredProject,
    EventDataTable,
    Project,
    ConstSecretResolver,
    TimeWindow,
    TimeGroup,
    DiscoverySettings,
    WebappSettings,
)
from mitzu.samples import get_sample_discovered_project

__version__ = "0.6.7"


__all__ = [
    "Connection",
    "ConnectionType",
    "Project",
    "EventDataTable",
    "DiscoveredProject",
    "ConstSecretResolver",
    "TimeWindow",
    "TimeGroup",
    "get_sample_discovered_project",
    "DiscoverySettings",
    "WebappSettings",
]


def load_from_project_file(
    project: str, folder: str = "./", extension="mitzu"
) -> DiscoveredProject:
    return DiscoveredProject.load_from_project_file(project, folder, extension)
