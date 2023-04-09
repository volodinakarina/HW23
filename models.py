from pydantic import BaseModel, validator

commands = ('filter', 'map', 'unique', 'sort', 'limit')


class RequestModel(BaseModel):
    """ Schema for request """
    cmd: str
    value: str

    @validator("cmd")
    def is_valid_command(cls, v):
        if v not in commands:
            raise ValueError(f'Bad request! Wrong command "{v}"')
        return v


class BatchRequestsModel(BaseModel):
    """ Schema for batch of requests """
    queries: list[RequestModel]
    file_name: str
