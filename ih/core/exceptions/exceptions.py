from fastapi import HTTPException


from ih.schema.common.error_response import ErrorResponse


class InventoryHeroAPIException(HTTPException):
    """
    Custom HTTPException that accepts the InventoryHero ErrorResponse model and automatically dumps it
    """
    def __init__(self, status_code: int, detail: ErrorResponse, **kwargs):
        super().__init__(status_code=status_code, detail=detail.model_dump(), **kwargs)
