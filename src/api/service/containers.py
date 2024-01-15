from dependency_injector import containers, providers
from api.service.participants_process import ParticipantsProcess
from api.persistance.meeting_repository import MeetingRepository
from api.persistance.notion_repository import NotionRepository
from api.persistance.slack_repository import SlackRepository
from api.persistance.notion_slack_mapping_repository import NotionSlackMappingRepository
from api.service.save_meeting_facade import MeetingProcess


class MeetingContainer(containers.DeclarativeContainer):
    meeting_repository = providers.Factory(MeetingRepository)
    notion_slack_mapping_repository = providers.Factory(NotionSlackMappingRepository)
    notion_repository = providers.Factory(NotionRepository)
    slack_repository = providers.Factory(SlackRepository)
    participants_process = providers.Factory(
        ParticipantsProcess,
        slack_repository=slack_repository,
        notion_slack_mapping_repository=notion_slack_mapping_repository,
    )
    meeting_process = providers.Factory(
        MeetingProcess,
        meeting_repository=meeting_repository,
        notion_slack_mapping_repository=notion_slack_mapping_repository,
        notion_repository=notion_repository,
        participants_process=participants_process
    )
