from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorObject(BaseModel):
    loc: List[str]
    msg: str
    type: str


class RestResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    errors: Optional[List[ErrorObject]] = None
    meta: Optional[Any] = None
    success: bool = True
    message: Optional[str] = None
