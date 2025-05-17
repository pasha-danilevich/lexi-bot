from aiogram_dialog.manager.manager import ManagerImpl


class CustomDialogManagerImpl(ManagerImpl):
    @property
    def service(self):
        return self.current_context().dialog_data['service']

    @property
    def dto(self):
        return self.current_context().dialog_data['dto']

    async def set_service(self, service) -> None:
        self.current_context().dialog_data['service'] = service

    async def set_dto(self, dto) -> None:
        self.current_context().dialog_data['dto'] = dto
