from dialog_manager.manager import CustomDialogManagerImpl



class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> None: # 'SomeService'
        return super().service

    @property
    def dto(self) -> None: # 'SomeDTO'
        return super().dto
