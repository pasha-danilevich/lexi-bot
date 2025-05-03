from dialogs.home.dto import HomeDTO
from dialogs.home.interface import DialogManager
from services.statistic.service import StatisticService


async def on_start(_, manager: DialogManager) -> None:
    await manager.set_service(service=StatisticService())
    user_id = manager.event.from_user.id
    statistic = await manager.service.get(user_id)
    await manager.set_dto(
        dto=HomeDTO(
            total_words=statistic.total_words,
        )
    )
