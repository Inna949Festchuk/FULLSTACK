from pydantic import BaseModel, field_validator 


class BasePress(BaseModel):
    title: str

    @field_validator("title")
    @classmethod 
    def check_title(cls, value: str):
        if len(value) >= 25:
            raise ValueError("Заголовок не должен содержать более 25 символов")
        return value

class CreatPress(BasePress):
    title: str
    body: str
    onwer: str 

class UpdatePress(BasePress):
    title: str or None = None
    body: str or None = None
    onwer: str or None = None
