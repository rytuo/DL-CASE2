from pydantic import BaseModel

class ModelRequestSchema(BaseModel):
    text: str


class ModelResponseSchema(BaseModel):
    texts: list[str]


class ModelVacancyResponseSchema(BaseModel):
    texts: list[str]
