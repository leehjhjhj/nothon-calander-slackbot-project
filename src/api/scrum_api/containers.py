from dependency_injector import containers, providers
from .scrum_process import ScrumProcess
from api.persistance.notion_repository import NotionRepository


class ScrumContainer(containers.DeclarativeContainer):
    notion_repository = providers.Factory(NotionRepository)
    scrum_process = providers.Factory(
        ScrumProcess,
        notion_repository=notion_repository
    )