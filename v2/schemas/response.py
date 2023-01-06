from pydantic import BaseModel


class ResponseFormat(BaseModel):
    status: int
    success: bool
    message: str
    data: dict


class CustomResponseFormat(BaseModel):
    status: int
    success: bool
    message: str
