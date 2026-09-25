from pydantic import BaseModel, ConfigDict


class NamedEntityResponseModel(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NamedEntityCreateModel(BaseModel):
    name: str


class NamedEntityUpdateModel(NamedEntityCreateModel):
    pass
