from pydantic import BaseModel, field_validator


class BaseUser(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("password is to short")
        return value


class CreatUser(BaseUser):
    name: str
    password: str


class UpdateUser(BaseUser):
    name: str | None = None
    password: str | None = None
