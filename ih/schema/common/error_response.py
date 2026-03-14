
from typing import Literal, List, Annotated
from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    loc: List[str|int]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Represents a single link in the breadcrumb trail."""
    message: str
    toast: bool = True
    toast_type: Literal["success", "info", "warning", "error"] = "error"

class FastAPIError(BaseModel):
    detail: List[ValidationErrorItem] | str | ErrorResponse

