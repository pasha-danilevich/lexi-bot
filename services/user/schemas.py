from pydantic import BaseModel, model_validator


class UserIdentifier(BaseModel):
    user_id: int | None = None
    telegram_id: int | None = None
    email: str | None = None

    @model_validator(mode='after')
    def validate_at_least_one_identifier(self) -> 'UserIdentifier':
        if not any([self.user_id, self.telegram_id, self.email]):
            raise ValueError(
                "At least one identifier must be provided (user_id, telegram_id or"
                " email)"
            )
        return self


class UserDTO(BaseModel):
    telegram_id: int


class UserSettings(BaseModel): ...
