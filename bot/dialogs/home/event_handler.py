from bot.dialogs.home.dto import HomeDTO
from bot.dialogs.home.interface import DialogManager
from services.statistic.service import StatisticService
from services.user.schemas import User


async def on_start(_, manager: DialogManager) -> None:
    user = User(id=manager.event.from_user.id)
    await manager.set_service(service=StatisticService(user))
    statistic = await manager.service.get_statistic()
    await manager.set_dto(
        dto=HomeDTO(
            total_words=statistic.total_words,
        )
    )
